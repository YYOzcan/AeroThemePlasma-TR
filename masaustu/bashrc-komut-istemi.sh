# Windows 7 Komut İstemi görünümü (AeroThemePlasma README önerisi).
# Yalnızca Konsole'un "Komut İstemi" profilinde (WIN7_CMD=1) devreye girer.
if [[ -n "$WIN7_CMD" ]]; then
    PS1='C:${PWD//\//\\\\}> '
    PROMPT_COMMAND='printf "\033]0;C:\\Windows\\system32\\cmd.exe\007"'
    echo -e "Microsoft Windows [Sürüm 6.1.7600]\nTelif Hakkı (c) 2009 Microsoft Corporation. Tüm hakları saklıdır.\n"
fi
