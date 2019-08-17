from bs4 import BeautifulSoup
from urllib.request import urlopen
from multiprocessing.dummy import Pool as ThreadPool
# import smtplib
# import ssl

# port = 587
# smtp_server = 'smtp.office365.com'
# password = 'password'
# sender = 'email-id'
# receiver = sender

base_url = "https://www.thehindu.com/archive/print/"
page = urlopen(base_url)
soup = BeautifulSoup(page, 'lxml')
inpt = open('dates', 'r')
output = open('2012-2019', 'w')


def getURL(url):
    try:
        page = urlopen(url)
    except Exception as e:
        print(e)
        return
    soup = BeautifulSoup(page, 'lxml')
    i = url.find('2')
    year = url[i:i + 4]
    month = url[i + 5: i + 5 + 2]
    day = url[i + 8: i + 8 + 2]
    date = year + month + day
    try:
        uls = soup.find_all('ul', {'class': 'archive-list'})
    except AttributeError:
        return
    for ul in uls:
        for li in ul.find_all('li'):
            a_tag = li.find('a')
            href = a_tag.get('href')
            if ('crossword' in href) or ('weather' in href) \
                    or ('solution' in href) or ('bullion' in href) \
                    or ('stock' in href) or ('exchange' in href):
                return
            else:
                output.write(date + ' - ' + href)
                output.write('\n')


# subject = 'YEAR DONE - ' + str(base_year - 1)
# text = "TO GO - " + str(2019 - base_year + 1)
# message = 'Subject: {}\n\n{}'.format(subject, text)
# ctxt = ssl.create_default_context()
# with smtplib.SMTP(smtp_server, port) as server:
#     server.starttls(context=ctxt)
#     server.ehlo()
#     server.login(sender, password)
#     server.sendmail(sender, receiver, message)
urls = inpt.readlines()
pool = ThreadPool(20)
pool.map(getURL, urls)
pool.close()
pool.join()
