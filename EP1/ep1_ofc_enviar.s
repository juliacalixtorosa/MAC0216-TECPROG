;****************************************************************************** 
; MAC0216 - Técnicas de Programação I (2024)
; EP1 - Linguagem de Montagem
;
; Nome: Júlia Calixto Rosa
; NUSP: 13749490
;******************************************************************************

global _start 

;****************************************************************************** 
; Seção de declaração de variáveis inicializadas e constantes
;****************************************************************************** 
section .data				

;*************************************************
; Constantes
;*************************************************

; Descritores dos arquivos de entrada e saída padrão   
STDIN:  equ 0
STDOUT: equ 1

; Modos de abertura de arquivo (segundo parâmetro da syscall sys_open)
RDONLY: equ	0                 ; somente leitura
WRONLY: equ	1                 ; somente escrita
RDWR:   equ 	2             ; leitura + escrita
WRONLY_CREAT_TRUNC: equ  577  ; somente escrita + cria se não existe + trunca se existe

; Modo de permissão de acesso a arquivo (terceiro parâmetro da syscall sys_open)
PERMISSION_MODE: equ 438          ; permissões de leitura e escrita 

; Deslocamentos para os parâmetros e variáveis locais das funções
arg1: equ +16
arg2: equ +24


;*************************************************
; Variáveis
;*************************************************
input1_arq_entrada:  db "Digite o nome do arquivo de entrada: ", 0x0
input2_arq_saida:    db "Digite o nome do arquivo de saída: ", 0x0   

hex_chars: db '0123456789ABCDEF'        ; Tabela para conversão para hexadecimal

;****************************************************************************** 
; Seção de declaração de variáveis não inicializadas
;****************************************************************************** 
section .bss

nome_arq_entrada:   resb   256
nome_arq_saida:     resb   256
tam_max1:           equ $ - nome_arq_entrada
tam_max2:           equ $ - nome_arq_saida

fd_arq_entrada:     resb   8
fd_arq_saida:       resb   8

byte_arq:           resb   1

code_point:         resd   1

string_hexadecimal: resb   12

CONTADOR:              resb 1

;****************************************************************************** 
; Seção de texto (código do corpo do programa)
;******************************************************************************    
section .text
    
;******************************************************************************
; FUNÇÃO: escreve_string(char* buffer)
; Escreva uma string na saída padrão (STDOUT). A função supõe que a string é 
; finalizada com '\0' (código 0x0). Usa a sys_write.
; ENTRADA:
; - char* buffer: ponteiro para a string (ou seja, o endereço da sua posição de 
;                 memória inicial).
;******************************************************************************
escreve_string:
    ; salvar RBP do chamador e definir nova base
    push    rbp
    mov     rbp, rsp

    mov rbx, [rbp+16]               ; endereço da mensagem a ser escrita
    
    ; Printa a mensagem caracter por caracter 
    print:
        ; sys_write(stdout, mensagem, tamanho)
        mov rax, 1                 ; chamada da função sys_write
        mov rdi, STDOUT            ; descritor da saída padrão
        mov rsi, rbx               ; mensagem de saída
        mov rdx, 1                 ; tamanho a ser escrito 
        
        cmp byte [rbx], 0x0
        je acabou_msg 
        syscall
        inc rbx
        jmp print  

    acabou_msg:
        ; restaurar RBP
        pop     rbp
        ret

;******************************************************************************
; FUNÇÃO: le_string(char* buffer, int tam_max)
; Lê da entrada padrão (STDIN) uma sequência de caracteres finalizada por ENTER 
; (caracter 0xA) e armazena-a na memória, finalizando com '\0' (caractere 0x0).
; Usa a sys_read.  
; ENTRADAS:
; - char* buffer: endereço inicial do espaço de memória onde a função 
;                 armazenará a string lida.
; - int tam_max: a quantidade máxima de caracteres a serem lidos. Usado para 
;                evitar 'estouro' do buffer caso o usuário digite mais 
;                caracteres do que o espaço disponível para armazenamento.
; SAÍDA: 
; - Devolve no registrador RAX a quantidade de caracteres lidos.
;******************************************************************************
le_string: 
    ; salvar RBP do chamador e definir nova base
    push    rbp
    mov     rbp, rsp

    ;int read(int fd, void *buf, size_t count);
    mov rax, 0 		            ; chamada da função sys_read
    mov rdi, STDIN		        ; Descritor de arquivo 0 (entrada padrão)
    mov rsi, [rbp+16]	        ; ponteiro para o buffer (onde armazena o que leu)
    mov rdx, [rbp+24]		    ; le no máximo resb 256
    syscall

    ; restaurar RBP
    pop     rbp
    ret

;******************************************************************************
; FUNÇÃO:  abre_arquivo(char* nome_arquivo, int modo_abertura)
; Abre um arquivo. 
; Usa a sys_open (const char *pathname, int flags, mode_t mode).
; Obs.: No parâmetro mode da sys_open, passa o valor 438 (constante 
;       PERMISSION_MODE) como modo de permissão de acesso (que corresponde à
;       permissão de leitura e escrita).
; ENTRADAS: 
; - char* nome_arquivo: endereço inicial da string do nome (ou do caminho+nome)
; - int modo_abertura: valor 0 (constante RDONLY) para indicar abertura para 
;                      leitura ou valor 577 (constante WRONLY_CREAT_TRUNC) para 
;                      indicar abertura para escrita e criando o arquivo caso
;                      ele não exista ainda ou sobreescrevendo o conteúdo dele
;                      caso ele já exista.  
; SAÍDA: 
; - Devolve no registrador RAX o descritor do arquivo aberto.
;******************************************************************************
abre_arquivo: 
    ; salvar RBP do chamador e definir nova base
    push    rbp
    mov     rbp, rsp

    ; int open (const char *pathname, int flags, mode_t mode);	
	mov rax, 2		            ; numero da chamada ao sistema (open)
	mov rdi, [rbp+16]	        ; 1º parametro: caminho + nome do arquivo
	mov rsi, [rbp+24]		    ; 2º paramentro: modo de abertura 
	mov rdx, PERMISSION_MODE	; 3º parametro: permissão de acesso, 438
	syscall

    ; restaurar RBP
    pop     rbp
    ret

;******************************************************************************
; FUNÇÃO: fecha_arquivo(int descritor_arquivo)
; Fecha um arquivo aberto previamente. Usa a sys_close.
; ENTRADA:
; - int  descritor_arquivo: descritor do arquivo a ser fechado.
;******************************************************************************
fecha_arquivo:
    ; salvar RBP do chamador e definir nova base
    push    rbp
    mov     rbp, rsp

    ; Fecha os arquivos
    mov rax, 3                      ; número da sys_close
    mov rdi, qword [fd_arq_saida]   ; Descritor de arquivo de entrada
    syscall
    
    ; restaurar RBP
    pop     rbp
    ret

;******************************************************************************
; FUNÇÃO: le_byte_arquivo(int descritor_arquivo, char* byte_arq) 
; Lê um byte de um arquivo aberto previamente para leitura. Usa a sys_read.
; ENTRADAS:
; - int descritor_arquivo: descritor do arquivo aberto para leitura.
; - char* byte_arq: endereço da posição de memória onde será armazenado o byte
;                   lido do arquivo.
; SAÍDA: 
; - Devolve em RAX o número de bytes lidos (ou seja, o valor devolvido pela 
;   chamada à sys_read). 
;******************************************************************************
le_byte_arquivo:    
    ; salvar RBP do chamador e definir nova base
    push    rbp
    mov     rbp, rsp

    ;int read(int fd, void *buf, size_t count);
    mov rax, 0 		                    ; chamada da função sys_read
    mov rdi, [rbp+16]                   ; valor do descritor de arquivo 
    mov rsi, [rbp+24]      	            ; ponteiro para o buffer (string_hexadecimal)
    mov rdx, 1		                    ; le no máximo 1 byte 
    syscall

    ; restaurar RBP
    pop     rbp
    ret

;******************************************************************************
; verifica_qtd_bytes: 
; Analisa o último byte lido do arquivo. 
; Verifica se o byte atual identifica um code point analisando o primeiro bit nulo
; mais significativo. Ou se é a continuação de um code point.
;
; - Salva em CONTADOR a quantidade de bytes a mais necessários para a construção
;   do code point
; - Constrói o code point no rótulo resto_code controlando a próxima posição
;   para armazenar parte dos bits do code point.
;******************************************************************************
verifica_qtd_bytes:

    ; verifica se o bit mais significativo é 0
    mov al, [byte_arq]
    and al, 10000000b
    jz um_byte

    ; verfica se os 2 bita mais significativos são 10 (resto do code point)
    mov al, [byte_arq]
    and al, 01000000b
    jz resto_code

    ; verifica se os 3 bits mais significativos são 110
    mov al, [byte_arq]
    and al, 00100000b
    jz dois_byte

    ; verifica se os 4 bits mais significativos são 1110
    mov al, [byte_arq]
    and al, 00010000b
    jz tres_byte

    ; verifica se os 5 bits mais significativos são 11110
    mov al, [byte_arq]
    and al, 00001000b
    jz quatro_byte


    um_byte:
        ; salva o code point 
        xor eax, eax
        mov byte [CONTADOR], 0                  
        mov al, [byte_arq]
        add dword [code_point], eax
        ret

    resto_code:
        ; salva pedaço do code point
        xor eax, eax
        mov al, [byte_arq]    
        and al, 00111111b
        shl dword [code_point], 6
        add dword [code_point], eax
        ret

    dois_byte:
        ; salva pedaço do code point
        xor eax, eax
        mov byte [CONTADOR], 1                   
        mov al, [byte_arq]
        and al, 00011111b
        add dword [code_point], eax
        ret

    tres_byte:
        ; salva pedaço do code point
        xor eax, eax
        mov byte [CONTADOR],2                    
        mov al, [byte_arq]
        and al, 00001111b
        add dword [code_point], eax
        ret

    quatro_byte:
        ; salva pedaço do code point
        xor eax, eax
        mov byte [CONTADOR], 3                   
        mov al, [byte_arq]
        and al, 00000111b
        add dword [code_point], eax
        ret

;******************************************************************************
; FUNÇÃO: gera_string_hexadecimal(int valor, char* buffer)
; Converte um número em uma string com a representação em hexadecimal dele. Por
; ex., para o inteiro 128526 (11111011000001110b), a string em hexadecimal é 
; '0x1F60E'. A função finaliza a string gerada com um caractere de quebra de 
; linha '\n' (código 0xA) e com o '\0' (código 0x0).
; ENTRADAS:
; - int valor: o número inteiro a ser convertido.
; - char* buffer: endereço da posição inicial da região de memória previamente  
;                 alocada que receberá a string gerada na conversão. 
;******************************************************************************
gera_string_hexadecimal: 

    ; salvar RBP do chamador e definir nova base
    push    rbp
    mov     rbp, rsp          

    ; RECUPERANDO O VALOR DO CODE POINT NO EAX
    mov eax,[rbp+19]
    shl eax, 8
    mov eax,[rbp+18]
    shl eax, 8
    mov eax,[rbp+17]
    shl eax, 8
    mov eax,[rbp+16]

    mov ebx, eax        ; copia do valor do code point

    ; Inicialize os ponteiros e Início da string hexadecimal
    mov rdi, [rbp+24]    ; Ponteiro para a string hexadecimal
    mov byte [rdi], '0'   
    inc rdi              
    mov byte [rdi], 'x'   
    inc rdi              ; Ajuste para a posição onde o próximo dígito será escrito


    ; Ignora os grupos de 4 bits zeros à esquerda utilizando a técnica dos shifts.
    ; Analisa os 4 bits menos significativos do registrador eax.
    ; Registrador ebx armazena os bits que ainda faltam ser analisados.
    xor rcx, rcx
    pula_4bits_zero:
        shr eax, 28
        cmp eax, 0
        jne conversao_hex 
        inc rcx
        cmp rcx, 8          ; existem no máximo 8 grupos de 4 bits. 
        je tudo_zero        ; Então, trata se é tudo zero.
        shl ebx, 4
        mov eax, ebx
        jmp pula_4bits_zero
    
    tudo_zero:
        mov byte[rdi], '0'
        inc rdi
        jmp fim

    conversao_hex:
        preparaçao:
        ; rcx possui a quantidade de 4bits 0s a ser ignorados
        mov eax, ebx  


        ; A cada 4 bits converte no seu hexadecimal correspondente, 
        ; utilizando uma tabela de hexadecimais e armazena
        ; na "string_hexadecimal" que foi passada como parâmetro
        loop_conversao:
            shr eax, 28
            mov eax, [1*eax+hex_chars]
            mov byte [rdi], al
            inc rdi
            inc rcx
            cmp rcx, 8          ; verifico se já fiz todas conversões possíveis
            je fim
            shl ebx, 4
            mov eax, ebx
            jmp loop_conversao



    fim:
        ; finaliza com '\n' e '\0'
        mov  byte [rdi], 0x0A       ;'\n' 
        inc rdi
        mov byte [rdi], 0x0         ;'\0'  

        ; restaurar RBP
        pop     rbp
        ret
;******************************************************************************
; FUNÇÃO: grava_string_arquivo(int descritor_arquivo, char* buffer)
; Grava string em um arquivo previamente aberto para escrita. A função supõe 
; que a string é finalizada com '\n' (código 0xA) e com '\0' (código 0x0). 
; Usa a sys_write.
; ENTRADAS:
; - int descritor_arquivo: descritor do arquivo aberto para escrita.
; - char* buffer: ponteiro para a string (ou seja, o endereço da sua posição de 
;                 memória inicial).
;******************************************************************************
grava_string_arquivo:

    ; salvar RBP do chamador e definir nova base
    push    rbp
    mov     rbp, rsp

    xor rbx,rbx
    mov rbx, [rbp+24]                      ; endereço da string_hexadecimal
    
    escreve_char:

        cmp byte [rbx], 0x0                ; se for o final da string é pq acabou 
        je acabou_string 

        ; sys_write(fd, mensagem, tamanho)
        mov rax, 1                         ; chamada da função sys_write
        mov rdi, qword [rbp+16]            ; valor do descritor do arquivo de saída
        mov rsi, rbx                       ; caracter a ser escrito
        mov rdx, 1                         ; tamanho a ser escrito (de byte em byte)   
        syscall

        inc rbx
        jmp escreve_char  

    acabou_string:
        ; restaurar RBP
        pop     rbp
        ret

;******************************************************************************
; Início do Programa
;****************************************************************************** 
_start:

    ; De ínicio, solicita os nomes dos arquivos de entrada e saída, 
    ; faz a leitura desses nomes e abre os dois arquivos.

    push  input1_arq_entrada
    call escreve_string
      
    add   rsp, 8

    push tam_max1
    push nome_arq_entrada
    call le_string
    mov [nome_arq_entrada+rax-1], BYTE 0x0 ; retira o enter do nome do arquivo       
    add   rsp, 16

    push  input2_arq_saida
    call escreve_string       
    add   rsp, 8

    push tam_max2
    push nome_arq_saida
    call le_string
    mov [nome_arq_saida+rax-1], BYTE 0x0 ; retira o enter do nome do arquivo
    add   rsp, 16
    
    push RDONLY
    push nome_arq_entrada
    call abre_arquivo
    mov [fd_arq_entrada], rax
    add   rsp, 16

    push WRONLY_CREAT_TRUNC
    push nome_arq_saida
    call abre_arquivo
    mov [fd_arq_saida], rax
    add   rsp, 16

    xor ebx, ebx
    
    loop_le_code:
        
        ; Neste loop, faz a leitura de byte a byte do arquivo a depender do valor
        ; armazenado em "CONTADOR" e constrói o code point, ambos processos feito 
        ; na subrotina "verifica_qtd_bytes"


        ; chama le_byte_arquivo(int descritor_arquivo, char* byte_arq) 
        push byte_arq
        push qword [fd_arq_entrada]
        call le_byte_arquivo
        add  rsp, 16

        ; verifica se o byte lido é o final do arquivo
        cmp byte [byte_arq], 0x0
        je acabou_arquivo

        ; verifica quantos bytes para o code point
        call verifica_qtd_bytes

        ; verifica se já li os bytes necessários
        cmp bl, [CONTADOR]

        je converte_escreve

        inc rbx 

        jmp loop_le_code
    
    converte_escreve:

        ; Nesta etapa, após já ter construído o "code_point" no "loop_le_code"
        ; gera a "string_hexadecimal" e grava no arquivo.
        
        ; PASSANDO O VALOR DO CODE POINT
        xor rsi, rsi
        mov esi, [code_point]
        shl esi, 8
        mov esi, [code_point]
        shl esi, 8
        mov esi, [code_point]
        shl esi, 8
        mov esi, [code_point]
        
        ; chama gera_string_hexadecimal(int valor, char* buffer)
        push string_hexadecimal
        push rsi                       ; push do valor do code point
        call gera_string_hexadecimal
        add rsp, 16

        ; chama grava_string_arquivo(int descritor_arquivo, char* buffer)
        push string_hexadecimal
        push qword [fd_arq_saida]
        call grava_string_arquivo
        add rsp, 16
        
        ; volta pra ler mais byte
        xor rbx,rbx
        
        ; cortou o loop infinito 
        mov dword [code_point], 0
        mov byte [byte_arq], 0

        jmp loop_le_code
    
    acabou_arquivo:
     
        ; fecha_arquivo(int descritor_arquivo)
        push qword [fd_arq_entrada]
        call fecha_arquivo
        add rsp, 8

        push qword [fd_arq_saida]
        call fecha_arquivo
        add rsp, 8

                
        ;sys_exit(int status);
        mov rax,60	; numero da chamada ao sistema (sys_exit)
        mov rdi,0	; primeiro argumento: código de saída (0 = sucesso)
        syscall

