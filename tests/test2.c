#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void sigio_handler (int signum)
{
 printf("signal recieved!\n");
}

int main (void)
{
  struct sigaction sact = {0};
  sact.sa_handler  = sigio_handler;
  sigaction(SIGPOLL, &sact, NULL);
  for(;;);
}
