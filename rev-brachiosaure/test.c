#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>

int expend_str(const char *str1, const char *str2, char **out, int size)
{
    __asm(
        ".intel_syntax noprefix\n"
        "test    rdi, rdi\n"
        "jz      loc_2955\n"
        "push    r14\n"
        "xor     r8d, r8d\n"
        "push    r13\n"
        "push    r12\n"
        "mov     r12, rsi\n"
        "push    rbp\n"
        "push    rbx\n"
        "test    rsi, rsi\n"
        "jz      short loc_2949\n"
        "mov     rbp, rdi\n"
        "mov     edi, ecx\n"
        "mov     esi, 1\n"
        "mov     r13, rdx\n"
        "imul    edi, ecx\n"
        "mov     ebx, ecx\n"
        "movsxd  rdi, edi\n"
        "call    calloc\n"
        "movsxd  r11, ebx\n"
        "xor     edi, edi\n"
        "xor     esi, esi\n"
        "mov     [r13+0], rax\n"
        "mov     r8d, 1\n"
        "loc_28F6:\n"
        "cmp     ebx, esi\n"
        "jle     short loc_2949\n"
        "xor     edx, edx\n"
        "lea     r14, [rbp+rdi+0]\n"
        "loc_2901:\n"
        "lea     r10, [r12+rdx]\n"
        "xor     r9d, r9d\n"
        "xor     ecx, ecx\n"
        "loc_290A:\n"
        "mov     al, [r14+r9]\n"
        "mul     byte ptr [r10]\n"
        "inc     r9\n"
        "add     r10, r11\n"
        "add     ecx, eax\n"
        "cmp     ebx, r9d\n"
        "jg      short loc_290A\n"
        "mov     rax, [r13+0]\n"
        "add     rax, rdi\n"
        "mov     [rax+rdx], cl\n"
        "cmp     esi, edx\n"
        "jnz     short loc_2930\n"
        "dec     cl\n"
        "jmp     short loc_2932\n"
        "loc_2930:\n"
        "test    cl, cl\n"
        "loc_2932:\n"
        "setz    al\n"
        "inc     rdx\n"
        "movzx   eax, al\n"
        "and     r8d, eax\n"
        "cmp     ebx, edx\n"
        "jg      short loc_2901\n"
        "inc     esi\n"
        "add     rdi, r11\n"
        "jmp     short loc_28F6\n"
        "loc_2949:\n"
        "pop     rbx\n"
        "mov     eax, r8d\n"
        "pop     rbp\n"
        "pop     r12\n"
        "pop     r13\n"
        "pop     r14\n"
        "ret\n"
        "loc_2955:\n"
        "xor     r8d, r8d\n"
        "mov     eax, r8d\n"
        "ret\n"
        ".att_syntax\n");
}

int main(void)
{
    printf("Hello, world!\n");

    char data[] = "data to hash";
    char buffer[SHA512_DIGEST_LENGTH];
    SHA512(data, sizeof(data) - 1, buffer);
    printf("buffer: %s\n", buffer);

    char *out = NULL;
    int res = expend_str(buffer, buffer, &out, 8);

    printf("res: %d\n", res);
    printf("out: %s\n", out);
    return 0;
}