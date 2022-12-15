#include <stdlib.h>

int get_sign(int x) {
   if (x == 0)
      return 0;
   
   if (x < 0)
      return -1;
   else 
      return 1;
}

int main() {
   int a = rand() % 10;
   return get_sign(a);
}
