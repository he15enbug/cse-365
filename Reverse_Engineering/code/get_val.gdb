start
break *main+709
commands
    silent
    set $rand_val = *(unsigned long long *)($rsi)
    printf "Current random value: %llx\n", $rand_val
    continue
end
continue