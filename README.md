
# Leitor de modelos de urna da eleição de 2022

Esse programa baixa os Dados de Urna diretamente do site do TSE para montar uma tabela que relaciona votos, modelos de urna, unidade federativa, município, zona e seção.

As tabelas (.csv) geradas pelo programa estão disponíveis nesse repositório na pasta csv

Caso queira produzir o seu próprio .csv por meio do programa, baixe apenas o arquivo main.py. 

Dois pacotes são necessários para rodar o programa: "py7zr" e "asn1tools". Lembre-se de instalar os pacotes antes de rodar o programa.

Os links dos Dados de Urna estão disponíveis no arquivo link.txt.
Cada arquivo zip dessa lista se refere aos dados de urna de um determinado turno em uma determinada unidade federativa.

# Como funciona?

1. O programa main.py seleciona um link do arquivo links.txt baixando os dados de urna
2. Para cada urna presente no arquivo .zip, extrai o LOG (.logjez)
3. Extrai o arquivo logd.dat do arquivo .logjez utilizando o pacote py7zr
4. Procura pelo modelo de urna no arquivo logd.dat
5. Lê o arquivo de boletim de urna (.bu) utilizando o decodificador disponibilizado pelo próprio TSE (bu_dump.py e bu.asn1) no link https://www.tse.jus.br/eleicoes/eleicoes-2022/documentacao-tecnica-do-software-da-urna-eletronica o qual utiliza o pacote asn1tools.
6. Registra os votos e os modelo da urna
7. Produz a tabela em formato .csv
8. Deleta o arquivo .zip baixado
9. Avança para o próximo link em links.txt

# Como utilizar?

Cada arquivo zip disponível no TSE representa uma unidade federativa em um determinado turno.

Por exemplo, o link https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2022/arqurnatot/bu_imgbu_logjez_rdv_vscmr_2022_1t_AC.zip serve para baixar o arquivo bu_imgbu_logjez_rdv_vscmr_2022_1t_AC.zip, cujo nome termina com 1t_AC, que se refere a primeiro turno (1t) e Acre (AC).

O programa baixa o arquivo zip automaticamente e realiza a leitura dos dados da urna. Se você já possui os arquivos .zip baixados, basta move-los para o mesmo diretório do programa antes de executá-lo.

Caso queira produzir o .csv de detemrinado turno e unidade federativa, faça conforme o exemplo a seguir:

*** Para baixar os dados do segundo turno de Alagoas:

    python main.py 2 'AL'

*** Nesse exemplo, o programa realizará a procura do arquivo bu_imgbu_logjez_rdv_vscmr_2022_2t_AL.zip ou realizará o download a partir da lista de links. Em seguida, produzirá o arquivo bu_imgbu_logjez_rdv_vscmr_2022_2t_AL.csv
  
# Observações

1. O Estado de São Paulo possui o maior arquivo zip de dados de urna, em torno de 20GB. Certifique-se de possuir espaço disponível no seu computador para o programa baixar o arquivo.

2. O programa exclui o arquivo .zip após a produção do .csv
