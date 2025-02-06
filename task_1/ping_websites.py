import os

from ping3 import ping

def count_rtts() -> tuple[list]:
    websites = ["google.com", "nsu.ru", "youtube.com", "vk.com", "ok.ru",
                "ru.wikipedia.org", "web.telegram.org", "dns-shop.ru",
                "ozon.ru", "wildberries.ru"]

    rtts = []
    for website in websites:
        rtt = ping(website)
        if rtt == None:
            rtts.append("No answer")
        else:
            rtts.append(rtt)

    return websites, rtts

def write_csv(output_file, websites, rtts) -> None:
    output_file.write("Website;RTT in seconds\n")
    for i in range(10):
        output_file.write(websites[i] + ';' + str(rtts[i]) + '\n')

def main() -> None:
    print("Enter output filename: ", end='')
    output_file = open(input(), "w")
    websites, rtts = count_rtts()
    write_csv(output_file, websites, rtts)
    print("RTTs have been saved")

main()