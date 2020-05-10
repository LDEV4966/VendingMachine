'''
클래스 실습 자판기 만들기
'''
import sys
#가격은 100원 단위이므로 PRICE_UNIT 상수 값을 100으로 선언한다
PRICE_UNIT = 100

class texts : 
    title = "#### 클래스 %s 자판기 입니다. ####"
    product = "%s:%s(%s원)"
    insert_coin = "동전을 넣어주세요 : "
    n_enough_coin = "동전이 부족합니다.\n거스름돈은 %s원 입니다"
    select_product = "원하시는 상품번호를 입력하세요"
    select_fault = "잘 못 누르셨습니다"
    product_out = "선택하신 상품의 가격은 %s 입니다. 거스름돈은 %s 입니다."

class Product :
    #제품 종류 , 가격을 코드 변경 없이 데이터를 쉽게 추가하거나 변경 가능
    ProductType = {}
    ProductValue = {}

class CoffeeVM(Product) :
    
    
    _name = "커피"#global변수로 선언
    _product_info_file = "coffee.txt"#global변수로 선언
    
    def __init__(self):
        #사용자가 자판기 종류를 선택하면 _name 출력한다
        print(texts.title %self._name)
    def set_products(self):
        #제품 종류, 가격 리스트를 초기화 한다
        Product.ProductType = {}
        Product.ProductValue = {}
        with open(self._product_info_file,"r",encoding="UTF-8") as fd :
            for line in fd :
                list = line.strip("\n").split(',')
                Product.ProductType[list[0]] = list[1]
                Product.ProductValue[list[0]]= int(list[2])
    def run(self):
        print(self._product_info_file)
        self.set_products()
        while True :
            try :
                inputCoin = float(input(texts.insert_coin))
            except ValueError :#잘 못된 값을 받으면 에러 메세지를 출력한다
                print(texts.select_fault)
            if inputCoin <= 0:
                print(texts.select_fault)
            else :
                self.select_product(inputCoin)

    def select_product(self,coin):
        #제품종류를 리스트로 선언하여 코드변경없이 데이터를 동적으로 보여준다
        description = ''
        for selection,item in Product.ProductType.items() :
            #제품과 가격을 가져온다 
            price = self.getProductValue(selection)
            description += selection+':'+item+'('+str(price)+'원) '
        print(description)
        inputProduct = input(texts.select_product)
        productValue = self.getProductValue(inputProduct)
        
        #입력한 값에 해당하는 내용이 리스트에 없으면 0이 반환된다
        if productValue:
            productName = self.getProductName(inputProduct)
            self.payment(coin,productName,productValue)
        else:
            #잘못된 값을 입력 받으면 에러 메세지를 출력하고 제품선택메뉴로 돌아간다.
            print(texts.select_fault)
            self.select_product(coin)#다시 입력하게 돌아간다
            
    def getProductValue(self,product):
        returnValue = 0
        for selection , value in Product.ProductValue.items():
            if selection == product:
                returnValue = value
        return returnValue 
    
    def getProductName(self,product):
        for selection , name in Product.ProductValue.items():
            if selection == product:
                return name
    def payment(self,coin,name,value) :
        coinValue = coin * PRICE_UNIT
        if coinValue >= value:
            balance = coinValue - value
            print(texts.product_out %(name,int(balance)))
        else :
            print(texts.n_enough_coin %int(coinValue))
            #지불을 마치면 초기메늃 이동한다
            self.run()
            
class SnackVM(CoffeeVM): #과자 클래스는 커피 클래스를 상속한다
    
    _name = "과자"#global변수로 선언
    _product_info_file = "snack.txt" #global변수로 선언
    def __init__(self):
        #Product 제품 종류, 가격을 Overriding한다.
        print(texts.title %self._name)
        
#############################################################
if __name__ == '__main__' :
    print("1:커피 , 2:과자")
    select_vm = input("구동할 자판기를 선택하세요.").strip()
    
    if select_vm == "1" :
        vm = CoffeeVM()
    elif select_vm == "2" :
        vm = SnackVM()
    else : 
        print("잘 못 누르셨습니다. 다시 실행 해 주세요.")
        sys.exit(0)#인자값이 0일 경우 이것은 프로그램의 “성공적 종료”로 간주. 0이 아닌 다른 값에선, 쉘 등으로 인한 “비정상 종료”로 간주
        
    try : 
        vm.run()
    except KeyboardInterrupt as exc :# vm.run()을 실행 시키는 도중 KeyboardInterrupt 발생시 예외 처리로 종료 시킨다
        print("판매를 종료 합니다.")
        