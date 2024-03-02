start
display/16i $rip
set $rip=*win
nexti 6
set $rip=$rip+2
nexti 2
set $rip=$rip+2
continue