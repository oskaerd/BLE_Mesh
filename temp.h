/* 
    Przykładowo, jak macie z pomiaru temperatury że jest
    23.62 stopnia C to trzymacie to w floacie, więc żeby
    uzyskać wartość do wysłania należy zrobić coś takiego:
    float temp_f = 23.62;
    int16_t temp_u16t = (uint16_t)(100*temp_f);
    I wtedy wysyłany jest 2 bajtowy integer 2362
    Ma być bo 1) nie ma co przesyłać floata (4 lub 8 bajtów)
    gdzie większość będzie 0 a 2) nie wiem jak by było z inter
    pretowniem tego przez pythona a tak przejdzie na bank i
    se to już przez 100 podzielę
 */

typedef struct {
    uint8_t opc; // set to 0xB3
    uint16_t dev_id; // device address, id
            // na razie obojętnie co np. 0xBEEF
    int16_t temp; // temperature, cast to int, don't send 
                    // floats
    uint8_t humidity; // 0-100% więc 8 bitów starczy
    uint32_t pressure; // tak samo jak z temperaturą
    uint16_t lux;
    uint16_t voltage; // tu zakladalem że będzie wysyłane
        // coś w stylu 336 jeśli napięcie wynosi 3.36V
        // więc trzeba to poprzeliczać przed wysłaniem i
        // wysyłać tylko inty
} BLEM_measurement;