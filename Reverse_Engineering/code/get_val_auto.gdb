start
continue
break *main+577
commands
    silent
    set $rand_val = *(unsigned long long *)($rsi)
    printf "Current random value: %llx\n", $rand_val
    continue
end

break *main+620
commands
    # put the random number at the address where the input of scanf will be stored
    set *((uint64_t *) $rsi) = $rand_val
    # Set the format string of scanf a null string
    set *((uint8_t *) $rdi) = 0
    continue
end

continue