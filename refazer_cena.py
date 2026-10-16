# Refaz UMA cena no ComfyUI que o notebook já deixou ligado (mesmo fluxo de duas etapas do notebook).
# uso no terminal do Colab: python refazer_cena.py <nome> <url_da_foto> <semente> "<prompt>"
import glob, json, os, shutil, subprocess, sys, time, urllib.request, uuid

nome, url_foto, semente, prompt = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
QUANT = os.environ.get("QUANT", "Q4_K_M")
NEGATIVO = ("text, letters, subtitles, watermark, logo, american police car, police text, sheriff, blurry, static, "
            "still frame, deformed, extra limbs, extra fingers, melting, morphing, low quality, jpeg artifacts, flicker")
foto = f"{nome}_v2.png"
urllib.request.urlretrieve(url_foto, f"/content/ComfyUI/input/{foto}")


def comum():
    return {
        "7": {"class_type": "CLIPLoader", "inputs": {"clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors", "type": "wan"}},
        "8": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["7", 0]}},
        "9": {"class_type": "CLIPTextEncode", "inputs": {"text": NEGATIVO, "clip": ["7", 0]}},
        "10": {"class_type": "VAELoader", "inputs": {"vae_name": "wan_2.1_vae.safetensors"}},
        "11": {"class_type": "LoadImage", "inputs": {"image": foto}},
        "12": {"class_type": "WanImageToVideo", "inputs": {"positive": ["8", 0], "negative": ["9", 0], "vae": ["10", 0], "start_image": ["11", 0], "width": 832, "height": 480, "length": 81, "batch_size": 1}},
    }


def amostrar(modelo, lora, latente, ini, fim, ruido):
    return {
        "1": {"class_type": "UnetLoaderGGUF", "inputs": {"unet_name": modelo}},
        "3": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0], "lora_name": lora, "strength_model": 1.0}},
        "5": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["3", 0], "shift": 5.0}},
        "13": {"class_type": "KSamplerAdvanced", "inputs": {"model": ["5", 0], "add_noise": "enable" if ruido else "disable", "noise_seed": semente, "steps": 4, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "positive": ["12", 0], "negative": ["12", 1], "latent_image": latente, "start_at_step": ini, "end_at_step": fim, "return_with_leftover_noise": "enable" if ruido else "disable"}},
    }


def pedir(caminho, dados=None):
    req = urllib.request.Request("http://127.0.0.1:8188" + caminho, data=json.dumps(dados).encode() if dados else None, headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req).read())


def rodar(fluxo):
    r = pedir("/prompt", {"prompt": fluxo, "client_id": str(uuid.uuid4())})
    if r.get("node_errors"):
        sys.exit(json.dumps(r)[-2000:])
    pid = r["prompt_id"]
    while True:
        h = pedir(f"/history/{pid}")
        if pid in h and h[pid].get("status", {}).get("completed") is not None:
            break
        time.sleep(5)
    if h[pid]["status"].get("status_str") != "success":
        sys.exit(json.dumps(h[pid]["status"])[-2000:])


prefixo = f"{nome}_v2_s{semente}"
t0 = time.time()
f = comum()
f.update(amostrar(f"Wan2.2-I2V-A14B-HighNoise-{QUANT}.gguf", "wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors", ["12", 2], 0, 2, True))
f["14"] = {"class_type": "SaveLatent", "inputs": {"samples": ["13", 0], "filename_prefix": f"latents/{prefixo}"}}
rodar(f)
lat = sorted(glob.glob(f"/content/ComfyUI/output/latents/{prefixo}_*.latent"))[-1]
shutil.copy(lat, f"/content/ComfyUI/input/{os.path.basename(lat)}")
print(f"1ª etapa: {time.time() - t0:.0f} s", flush=True)
f = comum()
f["20"] = {"class_type": "LoadLatent", "inputs": {"latent": os.path.basename(lat)}}
f.update(amostrar(f"Wan2.2-I2V-A14B-LowNoise-{QUANT}.gguf", "wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors", ["20", 0], 2, 4, False))
f["15"] = {"class_type": "VAEDecode", "inputs": {"samples": ["13", 0], "vae": ["10", 0]}}
f["16"] = {"class_type": "SaveImage", "inputs": {"images": ["15", 0], "filename_prefix": prefixo}}
rodar(f)
saida = f"/content/videos/{prefixo}.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "16", "-i", f"/content/ComfyUI/output/{prefixo}_%05d_.png",
                "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", saida], check=True)
print(f"PRONTO {saida} em {time.time() - t0:.0f} s")
