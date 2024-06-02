from .voice import Voice
from .sound import Sound
from .speak import Text_To_Voice
from .navigate import Navigate
from .Data import *

class Product():
    
    def __init__(self,Frame_Width,Frame_Height) -> None:
        
        self.SOUND = Sound()
        
        self.VOICE = Voice()

        self.SPEAK = Text_To_Voice()

        self.NAVIGATE = Navigate(Frame_Width,Frame_Height)
        
        self.TARGET_PRODUCTS = []

        self.TARGET_PRODUCT = ""

        self.FOUND_PRODUCTS_POS ={}
        
        self.FOUND_PRODUCTS = []

        self.ALL_CURRENT_PRODUCT_POS = []
        
        pass
        
        
    def GetProductString(self,Products_Array):
        
        TEXT = ""
        
        for product in Products_Array:

            if product!="Point1":
            
                TEXT += product+","
            
        return TEXT
    
    def GetProductsFromText(self,Text) :

        if(Text==False):
            return False

        Products_List = []

        for Product in PRODUCT_LIST.keys():

            if Product in Text:

                Products_List.append(Product)

        if( len( Products_List ) > 0 ):

            
            return Products_List
        
        else:

            return False
        
    def SayCurrentTargets(self):

        ProductString = self.GetProductString(self.TARGET_PRODUCTS)

        if ( ProductString == "" ):

            self.SPEAK.ThreadSpeak("現在沒有任何目標商品")

        else :

            self.SPEAK.ThreadSpeak("現在目標商品包括,"+ProductString)

    def GetCorrectProductPosAdvice(self,X):

        for Product in self.ALL_CURRENT_PRODUCT_POS:

            if(Product["Name"] == self.TARGET_PRODUCT):

                if(Product["X"] < X):

                    self.SPEAK.Say(f"目標商品{self.TARGET_PRODUCT} 喺左邊")
                
                else:

                    self.SPEAK.Say(f"目標商品{self.TARGET_PRODUCT} 喺右邊")




    def FindProduct(self,Input_Text = "",c = 1):

        self.SOUND.ThreadPlaySound("Note-1")

        Input_Products_List = self.GetProductsFromText(Input_Text)

        if ( not Input_Products_List ):

            if( c==1 ):

                self.SPEAK.Say(text="想搵啲乜嘢商品？")

                self.SOUND.ThreadPlaySound("Note-1")

            Input_Text = self.VOICE.StartCantonese(Text="",limit=40)

            Input_Products_List = self.GetProductsFromText(Input_Text)

            print(Input_Products_List)

            if Input_Text == False or Input_Text == "":
                
                if( c<3 ):

                    self.SOUND.ThreadPlaySound("Note-1")

                    self.SPEAK.Say(text="唔好意思,聽唔清楚,可以再講多次嗎？")

                    self.FindProduct(Input_Text="",c=c+1)

                else:

                    self.SOUND.ThreadPlaySound("Note-1")

                    self.SPEAK.ThreadSpeak(text="唔好意思,都係聽唔清楚, 請稍後再試")

        if Input_Products_List:

            result = Input_Products_List

            ProductList = []

            for product_name in result:

                if(product_name in self.TARGET_PRODUCTS):

                    self.SPEAK.ThreadSpeak("已經搵緊呢個物品")

                elif(product_name in PRODUCT_NAME_LIST ):

                    if(product_name in RECOMAND_LIST.keys()):

                        self.SOUND.ThreadPlaySound("Note-1")

                        self.SPEAK.Say(f"有第二隻同類商品{RECOMAND_LIST[product_name][0]}, 抵過{product_name} {RECOMAND_LIST[product_name][1]} 蚊喎, 要唔要改買呢個？")

                        self.SOUND.ThreadPlaySound("Note-1")

                        if self.VOICE.Confirm() :

                            product_name = RECOMAND_LIST[product_name][0]

                            self.SOUND.ThreadPlaySound("Note-1")

                            self.SPEAK.ThreadSpeak(f"好,成功將物品更改為{product_name}")

                            
                        else:

                            self.SOUND.ThreadPlaySound("Note-1")

                            self.SPEAK.ThreadSpeak(f"冇問題, 維持原本物品{product_name}")

                    ProductList.append(product_name)

                else:

                    self.SOUND.ThreadPlaySound("Error")

                    self.SPEAK.ThreadSpeak(f"目標商品{product_name}不存在")

            if(len(ProductList) == 0):

                return False

            ProductList = self.NAVIGATE.ShortProductsByLocations(ProductList)

            for product in ProductList:

                self.TARGET_PRODUCTS.append(product)

            Products_Text = self.GetProductString(self.TARGET_PRODUCTS)

            self.SOUND.ThreadPlaySound("Note-1")

            # self.SPEAK.ThreadSpeak(f"已經幫你由近到遠的區域重新排序商品")

            self.SPEAK.ThreadSpeak(f"添加尋找物品{Products_Text} 成功")

            self.SOUND.ThreadPlaySound("Note-1")
            
            return self.TARGET_PRODUCTS #[Name]


    def CancelFindProduct(self):
        
        self.SOUND.ThreadPlaySound("Note-1")

        if( len(self.TARGET_PRODUCTS) == 0):

            self.SOUND.ThreadPlaySound("Error")

            self.SPEAK.ThreadSpeak("目前沒有任何目標商品")

            return

        self.SPEAK.Say("想取消咩商品,現在目標商品包括")
        
        Products_Text = self.GetProductString(self.TARGET_PRODUCTS)
        
        self.SPEAK.Say(Products_Text)
        
        self.SOUND.ThreadPlaySound("Note-1")
        
        DEL_PRODUCTS = []
        
        Text = self.VOICE.StartCantonese(Text="")
        
        for Product in self.TARGET_PRODUCTS :
            
            if ( Product in Text ) :
                
                DEL_PRODUCTS.append(Product)

        if( len(DEL_PRODUCTS) >= 1 ):
                
            self.SOUND.ThreadPlaySound("Note-1")
                    
            self.SPEAK.Say("是否確認刪除商品")
            
            DEL_PRODUCTS_STRING = self.GetProductString(DEL_PRODUCTS)
            
            self.SPEAK.Say(DEL_PRODUCTS_STRING)

            self.SOUND.ThreadPlaySound( Type = "Note-1")
            
            if ( self.VOICE.Confirm() ) :
                
                for Product in DEL_PRODUCTS :
                    
                    INDEX = self.TARGET_PRODUCTS.index(Product)
                    
                    self.TARGET_PRODUCTS.pop(INDEX)

                if(len(self.TARGET_PRODUCTS) == 1 and self.TARGET_PRODUCTS[0] == "Point1"):

                    self.TARGET_PRODUCTS = []
                    
                self.SPEAK.ThreadSpeak("成功刪除商品.")
                
                self.SOUND.ThreadPlaySound("Note-1")

                self.TARGET_PRODUCTS = self.NAVIGATE.ShortProductsByLocations(self.TARGET_PRODUCTS)

            else:

                self.SPEAK.ThreadSpeak("取消刪除商品.")
                
                self.SOUND.ThreadPlaySound("Note-1")

            return self.TARGET_PRODUCTS
        
        else:

            self.SPEAK.ThreadSpeak("沒有該商品")

            self.SOUND.ThreadPlaySound("Note-1")
        
    def SayDiscount(self):

        for i in EVENT_DISCOUNT_LIST:

            self.SPEAK.ThreadSpeak(i)
            
        return



    def CheckIfTargetObj(self,Object_Name):
        if( Object_Name == self.TARGET_PRODUCT) : 

            del self.FOUND_PRODUCTS_POS[Object_Name]
                            
            self.FOUND_PRODUCTS.pop(self.FOUND_PRODUCTS.index(Object_Name))

            self.TARGET_PRODUCTS.pop(self.TARGET_PRODUCTS.index(Object_Name))

            self.TARGET_PRODUCT = ""    

            return True
        
        return False


        
    def ChooseTargetProducts( self,Count = 1 ):

        if(self.FOUND_PRODUCTS[0]=="Point1"):
            self.FOUND_PRODUCTS.pop(0)
            return

        if( len(self.FOUND_PRODUCTS) == 1 ):

            self.TARGET_PRODUCT = self.FOUND_PRODUCTS[0]

            self.SOUND.ThreadPlaySound( Type = "Note-1")

            self.SPEAK.Say( text = f"搵到目標商品{self.TARGET_PRODUCT} 喺你前方")

            print(f"搵到{self.TARGET_PRODUCT}")

            return True
        
        elif ( Count <= 3):

            if( Count == 1):

                TEXT = f"搵到"

                for Obj in self.FOUND_PRODUCTS:

                    TEXT += f"{Obj},"

                TEXT += "你想搵邊個先？"

            else:

                TEXT = "唔好意思聽唔清楚, 再講多次呀，唔該! 你想搵"

                for Obj in self.FOUND_PRODUCTS:

                    TEXT += f"{Obj} 定係"
                
            self.SOUND.ThreadPlaySound( Type = "Note-1")

            self.SPEAK.Say( text = TEXT )

            self.SOUND.ThreadPlaySound( Type = "Note-1")

            UserInput = self.VOICE.StartCantonese(Text="")
            
            

            if( UserInput in self.FOUND_PRODUCTS ) : 

                self.TARGET_PRODUCT = UserInput

                return UserInput
            
            else :
                 
                self.ChooseTargetProducts(Count+1)
            
        else:

            TEXT = "等我幫你揀啦! 我哋搵咗"

            TEXT += f"{self.FOUND_PRODUCTS[0]} 先啦"

            self.SOUND.ThreadPlaySound( Type = "Note-1")

            self.SPEAK.Say( text = TEXT )

            self.SOUND.ThreadPlaySound( Type = "Note-1")

            self.TARGET_PRODUCT = self.FOUND_PRODUCTS[0]

            return self.TARGET_PRODUCTS

        return False