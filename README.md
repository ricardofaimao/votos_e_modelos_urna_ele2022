# Gerador de tabelas com votos por candidato e modelos de urna para eleição presidencial de 2022

 Caso esteja procurando as tabelas .csv já produzidas pelo programa, acesse a pasta "tabelas" ou acesse o link abaixo
    
https://github.com/ricardofaimao/votos_e_modelos_urna_ele2022/tree/main/tabelas

# Sobre o programa

Esse programa baixa os DADOS DE URNA diretamente do site do TSE para montar uma tabela que relaciona votos, modelos de urna, unidade federativa, município, zona e seção.

Dois pacotes são necessários para rodar o programa: "py7zr" e "asn1tools". Lembre-se de instalar os pacotes antes de rodar o programa.

    pip install py7zr
    pip install asn1tools

Os links dos DADOS DE URNA estão disponíveis no arquivo links.txt.
Cada arquivo .zip dessa lista se refere aos dados de urna de um determinado turno em uma determinada unidade federativa.

# Como funciona

O programa mains.py percorre as seguintes etapas:

1. Seleciona um link do arquivo links.txt baixando os DADOS DE URNA de todas as seções de uma unidade federativa de um determinado turno (.zip)
2. Para cada urna presente no arquivo .zip, extrai arquivo LOG DE URNA (.logjez)
3. Extrai o arquivo logd.dat do arquivo .logjez utilizando o pacote py7zr
4. Procura pelo modelo de urna no arquivo logd.dat (arquivo que pode ser lido como arquivo de texto simples)
5. Lê o arquivo de boletim de urna (.bu) utilizando o decodificador disponibilizado pelo próprio TSE (bu_dump.py e bu.asn1) no link https://www.tse.jus.br/eleicoes/eleicoes-2022/documentacao-tecnica-do-software-da-urna-eletronica, o qual utiliza o pacote asn1tools.
6. Associa os votos com o modelo da urna
7. Produz a tabela em formato .csv
8. Deleta o arquivo .zip baixado
9. Avança para o próximo link em links.txt

# Como utilizar

Cada arquivo zip disponível no TSE representa uma unidade federativa em um determinado turno.

Por exemplo, o link https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2022/arqurnatot/bu_imgbu_logjez_rdv_vscmr_2022_1t_AC.zip serve para baixar o arquivo bu_imgbu_logjez_rdv_vscmr_2022_1t_AC.zip, cujo nome termina com 1t_AC, que se refere a primeiro turno (1t) e Acre (AC).

O programa baixa o arquivo zip automaticamente e realiza a leitura dos dados da urna. Se você já possui os arquivos .zip baixados, basta move-los para o mesmo diretório do programa antes de executá-lo.

*** Para produzir todos os arquivos .csv, basta executar o comando a seguir:

    python main.py

Caso queira produzir o .csv de detemrinado turno e unidade federativa, faça conforme o exemplo a seguir:

*** Para baixar os dados do segundo turno de Alagoas:

    python main.py 2 'AL'

*** Nesse exemplo, o programa realizará a procura do arquivo bu_imgbu_logjez_rdv_vscmr_2022_2t_AL.zip ou realizará o download a partir da lista de links. Em seguida, produzirá o arquivo bu_imgbu_logjez_rdv_vscmr_2022_2t_AL.csv
  
# Observações

1. Caso queira refazer um arquivo .csv, primeiro certifique-se de que não exista no diretório do programa um arquivo .csv com o mesmo nome do arquivo .zip.

2. O Estado de São Paulo possui o maior arquivo zip de dados de urna, em torno de 20GB. Certifique-se de possuir espaço disponível no seu computador para o programa baixar o arquivo.

3. O programa exclui o arquivo .zip após a produção do .csv
