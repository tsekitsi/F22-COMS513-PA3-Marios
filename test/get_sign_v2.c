#include <stdlib.h>

int get_sign(int x) {
   if (x == 0)
      { return 0; }
   
   if (x < 0)
      { return -2; }
   else 
      { return 2; }
}

int main() {
   *(int*)0 = 0; // bug-inducing change
   int a = rand() % 10;
   return get_sign(0);
}
