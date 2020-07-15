import requests # istek yapmak için 
from bs4 import BeautifulSoup # html içeriğini parçalayarak kullanabilmek için
import urllib.request # dosya indirmede kullanmak için
import os.path # kayıt işleminde dizin oluşturmak için

# Sonrasında istek yaparken kullanacağımız headerımızı tanımlayalım.
headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

# Şimdi bir değişken oluşturarak süper lig takımlarının listesinin bulunduğu adresi içerisine atayalım.
pageLeagueA = 'https://www.transfermarkt.com.tr/super-lig/startseite/wettbewerb/TR1'

# Sonrasında web servis isteğimizi gerçekleştiriyoruz. Gelen içeriği BeautifulSoup’a parametre olarak veriyoruz. 
# İkinci parametre olarak da html.parser seçeneğini veriyoruz.
treeLeagueA = requests.get(pageLeagueA, headers = headers)
soupLeagueA = BeautifulSoup(treeLeagueA.content, 'html.parser')

# Etiket üzerinde döngü ile veri elde etmeden önce bu verileri tutacak birkaç dizi oluşturacağız. 
# Bu diziler oyuncu adları, resim linkleri, takım adları ve takım id değerleri için yer alacak.
playerNames = []
playerImageLinks = []
teamNamesA = []
teamIdsA = []

# Dizileri de tanımladıktan sonra artık soupLeagueA objesinin fonksiyonlarını kullanabiliriz. 
# Kullanacağımız fonksiyon finAll() fonksiyonu olacak. Bu fonksiyon ile belirttiğimiz etiket değeri ve 
# class özelliğine sahip tüm değerleri bir dizi şeklinde alabileceğiz.

# Bu işlemi öncelikle takım adlarını ve id değerlerini almak için uygulayacağız.
# Aşağıdaki döngüde <td> etiketi ve class değeri olarak da 'hauptlink no-border-links hide-for-small hide-for-pad’ 
# değerini parametre olarak findAll() fonsiyonuna verdik. Sonrasında bu etiket içerisinde yer alan <a> etiketini 
# kullanarak href özelliğinde yer alan değeri elde ettik. Daha önceden bu değeri elde edip parçalayacağımızdan 
# bahsetmiştim. Parçalama işlemini ‘/’ karakterine göre yaptık. Parçalama sonucu bir dizi elde ettik. 
# Bu dizinin 1. indeksini takım adını almak, 4.indeksini de id değerini almak için kullandık. 
# Bu değerleri döngü içerisinde uygun biçimde teamNamesA dizisi ve temaIdsA dizisinde sonraki işlemlerde kullanmak 
# için depoladık.

for teamName in soupLeagueA.findAll('td', class_ = 'hauptlink no-border-links hide-for-small hide-for-pad'):
    if teamName.text != '':
        #print(teamName.find('a')['href'].split('/')[1])  
        teamNamesA.append(teamName.find('a')['href'].split('/')[1])
        #print(teamName.find('a')['href'].split('/')[4]) 
        teamIdsA.append(teamName.find('a')['href'].split('/')[4])

# Şimdi yine bir döngü kullanarak şuan ilgili takımda yer alan (örneğin Galatasaray SK) ve başka takımlarda 
# kiralık oynayan oyuncuların verilerini istek yaparak elde edeceğiz. Sonrasında ise bu değerleri dizilere atayacağız. 
# Kiralık olan oyuncuların bulunduğu sayfanın linki üzerinde de benzer işlemleri yapacağız. 
# Her takım için yine değişen değerler takım adı ve id değeri olacak.

# Öncelikle herhangi bir diziyi (id veya name) kullanarak işlemleri döngü içerisine alıyoruz. 
# Takım sayısı ve id sayısı aynı olduğu için iki diziden birini kullanabiliriz.

for i in range(len(teamNamesA)):
    
    # Döngü her döndüğünde bir önceki takımın oyuncu isimleri ve resim linkleri için oluşturduğumuz dizileri boşalttık. 
    # Eğer bunun yapmasaydık örnek olarak ilk takımın oyuncuları ikinci takımda da bulunacaktı. 
    # Üç içinde iki ve bir de olacaktı vb.
    playerNames.clear()
    playerImageLinks.clear()
    
    # Bu işlemden sonra ilgili linkleri oluşturduk. pageA as kadro için, pageLoan kiralık oyuncular için.
    pageA = 'https://www.transfermarkt.com.tr/' + teamNamesA[i] + '/startseite/verein/' + teamIdsA[i]
    pageLoan = 'https://www.transfermarkt.com.tr/' + teamNamesA[i] + '/leihspieler/verein/' + teamIdsA[i]
    
    # Sonrasında isteklerimizi yaptık. İstek sonucu gelen içeriği parçalayarak ilgili objeye atadık. 
    # Yine takım ad ve id değerlerini elde ederken yaptığımız gibi bir döngü ile bu sefer findAll() fonksiyonuna 
    # <img> etiketini ve class özelliği olarak da 'bilderrahmen-fixed' ‘i parametre olarak verdik. 
    # Çünkü bu değerler sitede kullanılmıştı. 
    
    # Bulduğumuz her değerin boş olup olmadığını kontrol ettik. Sonrasında playerNames ve playerIds dizilerini 
    # bulduğumuz değerleri parçalayarak doldurduk. Burada gelen her değer bir <img> etiketi. 
    # <img> etiketinin title özelliğinin değerini playerNames dizisine (harici olarak ben boşlukları kaldırıp 
    # tüm stringi küçük harf yaptım), data-src ve src özelliğini de resim linkini elde etmede kullandık. 
    # Kiralık oyuncularda data-src yerine, img etiketinde kullanılmadığı için src özelliğini kullandık. 

    treeA = requests.get(pageA, headers = headers)
    treeLoan = requests.get(pageLoan, headers = headers)
    soupA = BeautifulSoup(treeA.content, 'html.parser')
    soupLoan = BeautifulSoup(treeLoan.content, 'html.parser')

    for playerName in soupA.findAll('img', class_ = 'bilderrahmen-fixed'):
        if playerName['title'] != '':
            #print(playerName['title'].replace(" ", "-").lower())  
            playerNames.append(playerName['title'].replace(" ", "-").lower())

    for playerName in soupLoan.findAll('img', class_ = 'bilderrahmen-fixed'):
        if playerName['title'] != '':
            #print(playerName['title'].replace(" ", "-").lower())  
            playerNames.append(playerName['title'].replace(" ", "-").lower())

    for playerImageLink in soupA.findAll('img', class_ = 'bilderrahmen-fixed'):
        #print(playerImageLink['data-src'].replace("small", "header"))
        playerImageLinks.append(playerImageLink['data-src'].replace("small", "header"))

    for playerImageLink in soupLoan.findAll('img', class_ = 'bilderrahmen-fixed'):
        #print(playerImageLink['src'].replace("small", "header"))
        playerImageLinks.append(playerImageLink['src'].replace("small", "header"))
    
    # Bütün bu değerleri elde ettikten sonra sıra bu verileri bilgisayarımıza kaydetmeye geldi. 
    # Takım adlarını klasör adlandırmasında, oyuncu adlarını resim adlandırmasında ve resim linklerini de dosyaları 
    # indirmek için kullanacağız.
    # Bu işlemler için yine bir döngü kullanacağız. Bu döngüyü oyuncu adları sayısı kadar döndüreceğiz.

    for j in range(len(playerNames)): 
        #print (playerNames[j] + ", " + playerImageLinks[j])

        # Ben dosyaları D sürücüsünde Documents\WebScraping\Transfermarkt dizininde saklayacağım. 
        # Siz isterseniz farklı bir dizin seçebilirsiniz. Dizin yolunu her defasında takımlara uygun olarak oluşturduk. 
        # Böyle bir yol olmaması durumda ilgili dizini oluşturmak için de bir kontrol yazdık. 
        # Son olarak bu dizine dosyaları indirerek kaydediyoruz. Bunun için urllib.request.urlretrieve fonksiyonuna 
        # indirilecek dosya linkini ve kaydedilecek dosya yolunu, dosya ismi ve uzantısıyla beraber parametre olarak verdik.
        path = "D:\\Documents\\WebScraping\\Transfermarkt\\" + teamNamesA[i] + "\\"
        
        if not os.path.isdir(path):
            os.mkdir(path)
            
        urllib.request.urlretrieve(playerImageLinks[j], path + playerNames[j] + '.png') 
