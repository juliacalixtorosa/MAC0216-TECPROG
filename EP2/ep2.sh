#!/bin/bash

##################################################################
# MAC0216 - Técnicas de Programação I (2024)
# EP2 - Programação em Bash
#
# Nome: Júlia Calixto Rosa
# NUSP: 13749490

######################### MAIN #########################
# Executa todo o loop da interação com o usuário

function main {

    TDS_OPCOES=$(opcoes_operacoes)
    VETOR_OPERACOES[arq_atual]="arquivocompleto.csv"
    VETOR_OPERACOES[arq_filtrado]=${ARQ_COM_FILTROS}

    # Já inicializa o arquivo filtrado como sendo o arquivo completo
    (cat ${DIR_DADOS}/${VETOR_OPERACOES[arq_atual]} | tail -n +2 ) > ${ARQ_COM_FILTROS}
    
    while true; do

        echo "Escolha uma opção de operação: "
        select OPCAO in $TDS_OPCOES; do

            case ${REPLY} in 
            1) selecionar_arquivo ;;
            2) adicionar_filtro_coluna ;;
            3) limpar_filtros_colunas ;;
            4) mostrar_duracao_media_reclamacao ;;
            5) mostrar_ranking_reclamacoes ;;
            6) mostrar_reclamacoes ;;
            7) echo "Fim do programa"; \
               echo "+++++++++++++++++++++++++++++++++++++++"; \
               rm ${VETOR_OPERACOES[arq_filtrado]}; exit 0  ;;
                #OBS AQUI
            *) echo "Opção inválida." ;;

            esac
            break

        done
        
    done
    #echo "+++++++++++++++++++++++++++++++++++++++"
    
}

############### PREPARA_ARQUIVOS ${ARG_ARQ_TXT} ###############
# Baixa os arquivos .csv pelas urls que estão no arquivo .txt
# no diretório "${DIR_DADOS}".
# Converte para UTF8 todos os arquivos .csv.
# Constrói um arquivo que é a junção de todos os outros .csv.

function prepara_arquivos {
    local ARG_ARQ_TXT=$1

    mkdir ${DIR_DADOS}

    wget -nv -i ${ARG_ARQ_TXT} -P ${DIR_DADOS}

    for ARQ_ORIG in ${DIR_DADOS}/*.csv; do

        ARQ_SAIDA=${ARQ_ORIG}_convertido
        iconv -f ISO-8859-1 -t UTF8 ${ARQ_ORIG} -o ${ARQ_SAIDA}

        mv ${ARQ_SAIDA} ${ARQ_ORIG}


    done

    # Constrói arquivo completo só com um cabeçalho
    PRIMEIRO_ARQ="true"
    for ARQ_CSV in ${DIR_DADOS}/*.csv; do
        if [ "${PRIMEIRO_ARQ}" == "true" ]; then
            cat ${ARQ_CSV} >> ${DIR_DADOS}/arquivocompleto.csv
            PRIMEIRO_ARQ="false"
        else
            (cat ${ARQ_CSV} | tail -n +2 ) >> ${DIR_DADOS}/arquivocompleto.csv
        fi

    done

}

######################### OPCOES_OPERACOES #########################
# Apenas retorna as opções de operações que o usuário pode realizar

function opcoes_operacoes {
    echo "selecionar_arquivo adicionar_filtro_coluna limpar_filtros_colunas \
    mostrar_duracao_media_reclamacao mostrar_ranking_reclamacoes \
    mostrar_reclamacoes sair"

}

######################### SELECIONAR_ARQUIVO #########################
# Permite o usuário selecionar um arquivo dentre os que foram baixados.

function selecionar_arquivo {

    ARQUIVOS=($(ls ${DIR_DADOS}))
    NUM_ARQ=${#ARQUIVOS[*]}

    while  true; do
        echo "Escolha uma opção de arquivo: "
        select ARQ_ESCOLHIDO in ${ARQUIVOS[*]}; do

            if [ ${REPLY} -ge 1 ] && [ ${REPLY} -le ${NUM_ARQ} ]; then

                VETOR_OPERACOES[arq_atual]=${ARQ_ESCOLHIDO}

                (cat ${DIR_DADOS}/${ARQ_ESCOLHIDO} | tail -n +2 ) > ${VETOR_OPERACOES[arq_filtrado]}

                VETOR_OPERACOES[filtros_aplicados]=""

                echo "+++ Arquivo atual: " ${VETOR_OPERACOES[arq_atual]}
                echo "+++ Número de reclamações:" $(qtd_reclamacoes)
                echo "+++++++++++++++++++++++++++++++++++++++"
                return
            
            else
                echo "Opção inválida, escolha novamente"
                echo "---------------------------------------"
                break 

            fi
        done
    done
}

######################### ADICIONAR_FILTRO_COLUNA #########################
# Permite o usuário selecionar uma das colunas do arquivo para aplicar 
# algum filtro.

function adicionar_filtro_coluna {
    local IFS=";"
    local VALORES_COL=""
    local ARQ_ATUAL=${DIR_DADOS}/${VETOR_OPERACOES[arq_atual]}
    local PRIMEIRA_LINHA=($(head -n 1 ${ARQ_ATUAL}))
    local NUM_COLUNAS=${#PRIMEIRA_LINHA[*]}

    echo "Escolha uma opção de coluna para o filtro: "

    select COLUNA_ESCOLHIDA in ${PRIMEIRA_LINHA[*]}; do
        if [ ${REPLY} -ge 1 ] && [ ${REPLY} -le ${NUM_COLUNAS} ]; then

            VALORES_COL=$(cat ${VETOR_OPERACOES[arq_filtrado]} | cut -d ';' -f${REPLY} | sort | uniq)

            aplica_filtro ${VALORES_COL[*]} ${COLUNA_ESCOLHIDA}
            
            echo "+++ Adicionado filtro:" ${VETOR_OPERACOES[filtro_aplicado_agr]}
            echo "+++ Arquivo atual:" ${VETOR_OPERACOES[arq_atual]}
            echo "+++ Filtros atuais:" 
            echo "${VETOR_OPERACOES[filtros_aplicados]}"
            echo "+++ Número de reclamações: " $(qtd_reclamacoes)
            echo "+++++++++++++++++++++++++++++++++++++++"
            break
        else
            echo "Opção inválida, escolha novamente"
            echo "---------------------------------------"

        fi
    done
}

#################### APLICA_FILTRO ${ARG_VALORES} ${ARG_COLUNA} ####################
# Permite o usuário escolher quais dos valores da coluna escolhida que deseja 
# aplicar o filtro. 

function aplica_filtro {
    local IFS="
"
    local VALORES_COL=($1)
    local COL_ESCOLHIDA=$2
    local ARQ_TEMP="temp_file.csv"
    local ARQ_ATUAL=${DIR_DADOS}/${VETOR_OPERACOES[arq_atual]}
    local NUM_VALS=${#VALORES_COL[*]}

    echo "Escolha uma opção de valor para" ${COL_ESCOLHIDA}:
    
    select VALOR_ESCOLHIDO in ${VALORES_COL[*]}; do
        if [ ${REPLY} -ge 1 ] && [ ${REPLY} -le ${NUM_VALS} ]; then
            VETOR_OPERACOES[filtro_aplicado_agr]="${COL_ESCOLHIDA} = ${VALOR_ESCOLHIDO}"
            string_filtros_aplicados
            grep ${VALOR_ESCOLHIDO} ${VETOR_OPERACOES[arq_filtrado]} > ${ARQ_TEMP}

            mv ${ARQ_TEMP} ${VETOR_OPERACOES[arq_filtrado]}
            break
        else
            echo "Opção inválida, escolha novamente"
            echo "---------------------------------------"

        fi
    done
}

#################### STRING_FILTROS_APLICADOS ####################
# Apenas constrói a string de quais filtros foram aplicados até
# aquele mommento.

function string_filtros_aplicados {

    if [ "${VETOR_OPERACOES[filtros_aplicados]}" == "" ]; then
        VETOR_OPERACOES[filtros_aplicados]="${VETOR_OPERACOES[filtro_aplicado_agr]}"
    else 
        VETOR_OPERACOES[filtros_aplicados]+=" | ${VETOR_OPERACOES[filtro_aplicado_agr]}"
    fi
}

####################### LIMPAR_FILTROS_COLUNAS #######################
# Limpa os filtros aplicados resetando as variáveis 
# VETOR_OPERACOES[arq_filtrado] e VETOR_OPERACOES[filtros_aplicados]

function limpar_filtros_colunas {
    (tail -n +2 ${DIR_DADOS}/${VETOR_OPERACOES[arq_atual]}) > ${VETOR_OPERACOES[arq_filtrado]}
    VETOR_OPERACOES[filtros_aplicados]=""
    
    echo "+++ Filtros removidos"
    echo "+++ Arquivo atual:" ${VETOR_OPERACOES[arq_atual]}
    echo "+++ Número de reclamações: " $(qtd_reclamacoes)
    echo "+++++++++++++++++++++++++++++++++++++++"
}

############### MOSTRAR_DURACAO_MEDIA_RECLAMACAO ###############
# Mostra para o usuário a média (em dias) de duração dentre as 
# reclamções do arquivo filtrado. Utiliza as colunas 
# "Data de abertura" e "Data do Parecer" do arquivo filtrado.

function mostrar_duracao_media_reclamacao {
    local IFS=';'
    local NUM_COLUNA_ABERTURA=$(acha_num_coluna "Data de abertura")
    local NUM_COLUNA_PARECER=$(acha_num_coluna "Data do Parecer")

    DATAS=$(cat ${VETOR_OPERACOES[arq_filtrado]} | cut -d ';' -f${NUM_COLUNA_ABERTURA},${NUM_COLUNA_PARECER})
    IFS_OLD=${IFS}
    IFS=''
    RESULTADO_MEDIA=$(retorna_media ${DATAS[*]})
    IFS=${IFS_OLD}
    
    echo "+++ Duração média da reclamação:" ${RESULTADO_MEDIA} "dias" 
    echo "+++++++++++++++++++++++++++++++++++++++"
    
}

#################### RETORNA_MEDIA ${ARG_DATAS} ####################
# Calcula e retorna a média (em dias) de duração das reclamações do 
# arquivo filtrado.
#
# OBS: não lida bem quando as datas estão nas colunas erradas.

function retorna_media {
    local IFS="
"
    local DATAS=($1)
    local SOMA_DIFERENCAS=0
    local DIFERENCA=0
    local QTD_RECLAMACOES=0

    for LINHA in ${DATAS[*]}; do
        DATA_ABERTURA=$( echo ${LINHA} | cut -d ';' -f1 )
        DATA_PARECER=$( echo ${LINHA} | cut -d ';' -f2 )

        DATA_ABERTURA=$(date -d "${DATA_ABERTURA}" +%s)
        DATA_PARECER=$(date -d "${DATA_PARECER}" +%s)

        DIFERENCA=$(echo "(${DATA_PARECER} - ${DATA_ABERTURA}) / 86400" | bc)
        SOMA_DIFERENCAS=$(echo "${SOMA_DIFERENCAS} + ${DIFERENCA}" | bc)
        QTD_RECLAMACOES=$(echo "${QTD_RECLAMACOES}"+1 | bc )
    done

    RESULTADOS[1]=${SOMA_DIFERENCAS}
    RESULTADOS[2]=${QTD_RECLAMACOES}
    MEDIA=$(echo "( ${RESULTADOS[1]} / ${RESULTADOS[2]} )" | bc )

    echo ${MEDIA}

}

############### ACHA_NUM_COLUNA ${ARG_COLUNA} ###############
# Encontra e retorna a posição de uma coluna que está na
# primeira linha do arquivo.

function acha_num_coluna {
    local NOME_COLUNA=$1
    local NUM=0
    local ARQ_ATUAL=${DIR_DADOS}/${VETOR_OPERACOES[arq_atual]}
    local PRIMEIRA_LINHA=($(head -n 1 ${ARQ_ATUAL}))

    for COLUNA in ${PRIMEIRA_LINHA[*]}; do
        NUM=$(echo "${NUM}"+1 | bc )

        if [ "${COLUNA}" == "${NOME_COLUNA}" ]; then
            break
        fi
    done

    echo ${NUM}
}

############### MOSTRAR_RANKING_RECLAMACOES ###############
# Mostra as Top 5 reclamações do arquivo filtrado.

function mostrar_ranking_reclamacoes {
    local IFS=";"
    local ARQ_ATUAL=${DIR_DADOS}/${VETOR_OPERACOES[arq_atual]}
    local PRIMEIRA_LINHA=($(head -n 1 ${ARQ_ATUAL}))
    local NUM_COLUNAS=${#PRIMEIRA_LINHA[*]}
    local TOP5_RECLAMACOES=""
    
    echo "Escolha uma opção de coluna para análise:"

    select COLUNA_ESCOLHIDA in ${PRIMEIRA_LINHA[*]}; do
        if [ ${REPLY} -ge 1 ] && [ ${REPLY} -le ${NUM_COLUNAS} ]; then

            TOP5_RECLAMACOES=$(cat ${VETOR_OPERACOES[arq_filtrado]} | sed -E 's/( )+[0-9]+( )+//' \
                                | cut -d ';' -f${REPLY} | sort | uniq -c | sort -n -r | head -n 5)

            echo "+++ "${COLUNA_ESCOLHIDA}" com mais reclamações:"
            echo "${TOP5_RECLAMACOES}"
            echo "+++++++++++++++++++++++++++++++++++++++"
            break
        else
            echo "Opção inválida, escolha novamente"
            echo "---------------------------------------"

        fi
    done
}

######################## QTD_RECLAMACOES #######################
# Apenas retorna a quantidade de reclamções do arquivo filtrado.

function qtd_reclamacoes {
    local QTD_RECLAMACOES=$( cat ${VETOR_OPERACOES[arq_filtrado]} | wc -l )
    echo "${QTD_RECLAMACOES}"
}

######################## MOSTRAR_RECLAMCOES ########################
# Mostra todas as reclamções presentes do arquivo filtrado.

function  mostrar_reclamacoes {
    RECLAMACOES=$(cat ${VETOR_OPERACOES[arq_filtrado]})
    echo "${RECLAMACOES}"
    echo "+++ Arquivo atual:" ${VETOR_OPERACOES[arq_atual]}
    echo "+++ Filtros atuais:" 
    echo "${VETOR_OPERACOES[filtros_aplicados]}"
    echo "+++ Número de reclamações: " $(qtd_reclamacoes)
    echo "+++++++++++++++++++++++++++++++++++++++"

}

############################# VARIÁVEIS GLOBAIS #############################  
# VETOR_OPERACOES: espécie de dicionário que armazena os principais 
# valores do programa
#
# - VETOR_OPERACOES[arq_atual]: nome do último arquivo selecionado pelo usuário
#
# - VETOR_OPERACOES[arq_filtrado]: nome do arquivo que contém o resultado de 
#  todos os últimos filtros aplicados
#
# - VETOR_OPERACOES[filtro_aplicado_agr]: string do último filtro aplicado 
#
# - VETOR_OPERACOES[filtros_aplicados]: string com todos os filtros que 
# foram aplicados
#
# DIR_DADOS: nome do diretório onde será armazenado os dados baixados
#
# ARQ_COM_FILTROS: nome do arquivo que armazenará o resultado dos filtros

DIR_DADOS="dados"
ARQ_COM_FILTROS="arquivo_com_filtros.csv"

declare -A VETOR_OPERACOES=()
VETOR_OPERACOES[filtros_aplicados]=""

############### TRATAMENTO DE ERROS E MODO DE EXECUÇÃO ###############
# Modo de Execução: depende da quantidade de argumentos passados.
# E suporta no máximo 1 argumento.
#
# Tipo de Erros: 
# 1 - Se o arquivo .txt passado como argumento não existe
# 2 - Se os dados .csv não estão disponíveis no diretório "dados"

if [ $# -eq 1 ]; then
    ARQ_URLS_TXT=$1

    echo "+++++++++++++++++++++++++++++++++++++++" 
    echo "Este programa mostra estatísticas do"    
    echo "Serviço 156 da Prefeitura de São Paulo"  
    echo "+++++++++++++++++++++++++++++++++++++++"

    if [ ! -e ${ARQ_URLS_TXT} ]; then
        echo "ERRO: O arquivo ${ARQ_URLS_TXT} não existe."
        exit 1
    fi

    prepara_arquivos ${ARQ_URLS_TXT}

    if [ $( ls ${DIR_DADOS} | wc -l ) -eq 0 ]; then
        echo "ERRO: Não há dados baixados."
        echo "Para baixar os dados antes de gerar as estatísticas, use:" 
        echo "  ./ep2_servico156.sh <nome do arquivo com URLs de dados do Serviço 156>"
        exit 1
    fi

    main
    

elif [ $# -eq 0 ]; then

    echo "+++++++++++++++++++++++++++++++++++++++" 
    echo "Este programa mostra estatísticas do"    
    echo "Serviço 156 da Prefeitura de São Paulo"  
    echo "+++++++++++++++++++++++++++++++++++++++"

    if [ ! -d ${DIR_DADOS} ]; then
        echo "ERRO: Não há dados baixados."
        echo "Para baixar os dados antes de gerar as estatísticas, use:" 
        echo "  ./ep2_servico156.sh <nome do arquivo com URLs de dados do Serviço 156>"
        exit 1
    
    else        
        main
    fi

else
    echo "Erro: O script deve ser executado com no máximo 1 parâmetro"
    exit 1
fi



         