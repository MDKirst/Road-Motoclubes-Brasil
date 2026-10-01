[LEIA-ME.txt](https://github.com/user-attachments/files/32921620/LEIA-ME.txt)
COURO & ASFALTO - BR-277
Corrida de moto com briga em trechos reais da BR-277 (Paraná).

COMO JOGAR (Windows)
1. Descompacte o .zip numa pasta qualquer.
2. Dê dois cliques em JOGAR.bat.
   Abre uma janela preta (o servidorzinho local) e o jogo no navegador.
   Deixe a janela preta aberta enquanto joga; feche-a para desligar.
   Se o Windows avisar "o Windows protegeu o computador", clique em
   "Mais informações" > "Executar assim mesmo" (o script é texto puro:
   dá para abrir o servidor.ps1 no Bloco de Notas e conferir).

Por que não dá para abrir o index.html direto? O navegador bloqueia o jogo
de ler os arquivos das pistas quando a página é aberta como arquivo (file://).
O JOGAR.bat resolve isso servindo a pasta em http://localhost:8277.

Outra opção (se tiver Python): dentro da pasta "jogo", rode
   python -m http.server 8277
e abra http://localhost:8277 no navegador.

CONTROLES
Teclado: W/S acelera e freia · A/D inclina · J/K soco · L chute ·
Shift (ou W duas vezes) nitro · O óleo · Q olha para trás · R volta à pista ·
V som · Esc pausa · F3 dados técnicos. Caído: W/A/S/D anda até a moto.
Controle (Xbox/PlayStation): RT acelera · LT freia · analógico inclina ·
X/B soco · A chute · RB nitro · LB óleo · Y olha para trás · Start pausa.
Celular: botões na tela (melhor com o celular deitado; o celular precisa
abrir o jogo por um servidor ou pelo site publicado).

QUALIDADE GRÁFICA
No menu: "automática" escolhe pela placa de vídeo. Se travar, use "baixa".

FONTES E CRÉDITOS
Traçado: DNIT (SNV) · municípios: IBGE · relevo: SRTM/NASA ·
© contribuidores do OpenStreetMap · prédios: Overture Maps (ODbL) ·
personagens: Quaternius (CC0). Brasões pertencem aos respectivos motoclubes.
