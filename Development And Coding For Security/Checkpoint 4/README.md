# Ransomware com RSA
---

## Como funciona?
O código foi testado em sistemas Linux. O código funciona criptografando o arquivo "ENCRYPTME.txt" que é designado especialmente para testes.
Para que o código seja executado com sucesso é necessário que o arquivo seja criado, com algum conteúdo, seja ele qual for. Ao ser criptografado,
o arquivo vai aparentar estar em base64, isso ocorre para evitar erros na descriptografia, ou na escrita/leitura dos arquivos.

Após criptografar o arquivo, o diretório do qual o programa foi chamado vai conter dois novosa arquivos: LEIAME.txt & DECRYPTION_KEY.txt
O arquivo LEIAME.txt contém a mensagem informando o usuário do ocorrido na máquina, e como a vítima deve proceder para a recuperação dos arquivos.
O arquivo DECRYPTION_KEY.txt contém a chave RSA utilizada para descriptografar os arquivos, e se encontra presente apenas para motivos de demonstração.

## Como utilizar:
- Criar um arquivo de nome ENCRYPTME.txt no mesmo diretório em que se encontra o ransomware.
- Executar o comando `python ransomware.py` para criptografar o arquivo.
- Executar o comadno `python ransomware.py --decrypt CHAVE_DE_DESCRIPTOGRAFIA` para resturar o arquivo original.
