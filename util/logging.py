import datetime

date = datetime.datetime.now()


def start_logging(log_path):
    log_name = f"{date}-flaskchan.log"
    log = open(f"{log_path}/{log_name}", 'x')
    log.write("Start of the log!")
    log.close()
    return log


log_good = " [\033[1;32m*\033[0;0m]"
log_warn = " [\033[1;33m!\033[0;0m]"
log_error = " [\033[1;31mX\033[0;0m]]"


def log_config(cfg, log_name):
    print(f'{log_good} Starting with this parameters: {cfg}')
    if cfg['logging']:
        using_log = open(f"{log_name}", 'a')
        using_log.write(f"\n[GOOD] Starting with this parameters: {cfg}")
        using_log.close()
    else:
        print(f"{log_warn} Logging is disabled in config.json, so, this will not be written in .log file.")
