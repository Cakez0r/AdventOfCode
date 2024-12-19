#include <stdio.h>
#include <stdlib.h>

// #define PROGRAM_LENGTH 6
#define PROGRAM_LENGTH 16
#define BATCH_SIZE 0xFFFFFFFF // 1000000000

// This is the code that finally got me the answer for part 2...
int main()
{
    int program[] = {2, 4, 1, 1, 7, 5, 4, 7, 1, 4, 0, 3, 5, 5, 3, 0};
    unsigned long maxv = 0b111111111111111111111111111111111111111111;
    int last_p = 0;
    for (unsigned long i = 0; i < maxv; i++)
    {
        unsigned long A = (46ul << 42) | i;
        int n = 0;
        while (A)
        {
            unsigned long B = A & 0b111;
            B = B ^ 1;
            unsigned long C = A >> B;
            B = B ^ C;
            B = (B ^ 4) & 0b111;
            if (B != program[n])
            {
                break;
            }
            A = A >> 3;
            n++;
        }

        int p = (int)(((double)i / maxv) * 1000);
        if (p != last_p)
        {
            printf("%.1f pct\n", (float)p / 10);
            last_p = p;
        }
        if (n >= 15)
        {
            printf("FOUND: %lu (%d)\n", i, n);
        }
    }
}

// Everything after here is a failed brute force attempt and wasn't used to generate the final answer
typedef struct
{
    unsigned long A;
    unsigned long B;
    unsigned long C;
    int IP;
    int OP;
    int OUT[PROGRAM_LENGTH];
    int OUT_C;
} State;

int combo(State *s)
{
    if (s->OP == 4)
    {
        // printf("(A)\n");
        return s->A;
    }
    else if (s->OP == 5)
    {
        // printf("(B)\n");
        return s->B;
    }
    else if (s->OP == 6)
    {
        // printf("(C)\n");
        return s->C;
    }
    else
    {
        // printf("(%d)\n", s->OP);
        return s->OP;
    }
}

void adv(State *s)
{
    s->A = s->A >> combo(s);
}

void bdv(State *s)
{
    s->B = s->A >> combo(s);
}

void cdv(State *s)
{
    s->C = s->A >> combo(s);
}

void bxl(State *s)
{
    s->B = s->B ^ s->OP;
}

void bst(State *s)
{
    s->B = combo(s) & 0b111;
}

void jnz(State *s)
{
    if (s->A)
        s->IP = s->OP - 2;
}

void bxc(State *s)
{
    s->B = s->B ^ s->C;
}

void out(State *s)
{
    s->OUT[s->OUT_C] = combo(s) & 0b111;
    s->OUT_C++;
}

void step(State *s, int *program)
{
    int o = program[s->IP];
    s->OP = program[s->IP + 1];

    // bst 4: B = A
    // bxl 1: B = B ^ 1
    // cdv 5: C = A >> B
    // bxc 7: B = B ^ C
    // bxl 4: B = B ^ 4
    // adv 3: A = A >> 3
    // out 5: OUT B
    // jnz 0: GOTO 0
    switch (o)
    {
    case 0:
        // printf("adv %d\n", s->OP);
        adv(s);
        break;
    case 1:
        // printf("bxl %d\n", s->OP);
        bxl(s);
        break;
    case 2:
        // printf("bst %d\n", s->OP);
        bst(s);
        break;
    case 3:
        // printf("jnz %d\n", s->OP);
        jnz(s);
        break;
    case 4:
        // printf("bxc %d\n", s->OP);
        bxc(s);
        break;
    case 5:
        // printf("out %d\n", s->OP);
        out(s);
        break;
    case 6:
        // printf("bdv %d\n", s->OP);
        bdv(s);
        break;
    case 7:
        // printf("cdv %d\n", s->OP);
        cdv(s);
        break;
    }

    s->IP += 2;
}

int main2()
{
    // 11100101011000000
    // adv 3
    // out 4
    // jnz 0
    int batch = 0;
    int program[] = {0, 3, 5, 4, 3, 0};
    int len = sizeof(program) / sizeof(int);

    for (unsigned long i = 1; 1; i++)
    {
        unsigned long A = i;
        unsigned long B = 0;
        unsigned long C = 0;
        int outc = 0;
        int mismatch = 0;
        // 117440
        while (outc < len)
        {
            A = A >> 3;
            if ((A & 0b111) != program[outc])
            {
                mismatch = 1;
                break;
            }
            outc++;
        }

        if (!mismatch && outc == len)
        {
            printf("*** FOUND %d *** \n", i);
            return 0;
        }
    }
}

int mainY(int argc, char *argv[])
{
    // unsigned long batch = argc == 1 ? 0 : atol(argv[1]);
    // unsigned long batch_start = BATCH_SIZE * batch;
    // unsigned long batch_end = batch_start + BATCH_SIZE;
    unsigned long batch = 0;
    unsigned long batch_start = 0;
    unsigned long batch_end = 0xFFFFFFFFFFFFFFFF;
    int program[] = {2, 4, 1, 1, 7, 5, 4, 7, 1, 4, 0, 3, 5, 5, 3, 0};
    int len = sizeof(program) / sizeof(int);

    // bst 4: B = A
    // bxl 1: B = B ^ 1
    // cdv 5: C = A >> B
    // bxc 7: B = B ^ C
    // bxl 4: B = B ^ 4
    // adv 3: A = A >> 3
    // out 5: OUT B
    // jnz 0: GOTO 0
    int best = 0;
    for (unsigned long i = batch_start; i < batch_end; i++)
    // for (unsigned long i = 0; 1; i++)
    {
        unsigned long A = i;
        unsigned long B = 0;
        unsigned long C = 0;
        int outc = 0;
        int mismatch = 0;
        while (A && outc < len)
        {
            B = (A & 0b111);

            B = B ^ 1;
            C = A >> B;
            B = B ^ C;
            B = B ^ 4;

            A = A >> 3;

            if ((B & 0b111) != program[outc])
            {
                mismatch = 1;
                break;
            }
            outc++;
        }

        if (outc > best)
        {
            best = outc;
            printf("%lu: %d\n", i, best);
        }

        if (!mismatch && outc == len)
        {
            printf("*** FOUND %d *** \n", i);
        }
    }

    printf("Finished batch %d\n", batch);
}

int mainX(int argc, char *argv[])
{
    int batch = 0; // atoi(argv[1]);
    // int program[] = {0, 3, 5, 4, 3, 0};
    int program[] = {2, 4, 1, 1, 7, 5, 4, 7, 1, 4, 0, 3, 5, 5, 3, 0};

    // for (unsigned long i = BATCH_SIZE * batch; i < BATCH_SIZE * (batch + 1); i++)
    for (unsigned long i = 0; 1; i++)
    {
        State s = {0};
        s.A = i;
        int mismatch = 0;

        while (s.IP < PROGRAM_LENGTH && !mismatch)
        {
            step(&s, program);
            for (int j = 0; j < s.OUT_C; j++)
            {
                if (s.OUT[j] != program[j])
                {
                    mismatch = 1;
                    break;
                }
            }
        }

        if (s.OUT_C == PROGRAM_LENGTH)
        {
            printf("*** FOUND %d ***\n", i);
            return 0;
        }
    }

    printf("Finished batch %d\n", batch);
    return 0;
}