from .voice import Voice
from .sound import Sound
from .speak import Text_To_Voice
from .Data import *

class Product():
    
    def __init__(self) -> None:
        
        self.SOUND = Sound()
        
        self.VOICE = Voice()

        self.SPEAK = Text_To_Voice()
        
        self.TARGET_PRODUCTS = []

        self.TARGET_PRODUCT = ""

        self.FOUND_PRODUCTS_POS ={}
        
        self.FOUND_PRODUCTS = []
        
        pass
        
        
    def GetProductString(self,Products_Array):
        
        TEXT = ""
        
        for product in Products_Array:
            
            TEXT += product+","
            
        return TEXT

    def FindProduct(self,c = 1):

        self.SOUND.ThreadPlaySound("Note-1")

        if( c==1 ):

            self.SPEAK.Say(text="想搵啲乜嘢商品？")

            self.SOUND.ThreadPlaySound("Note-1")

        Text = self.VOICE.StartCantonese(Text="",limit=40)

        if Text == False or Text == "":
            
            if( c<3 ):

                self.SOUND.ThreadPlaySound("Note-1")

                self.SPEAK.Say(text="唔好意思,聽唔清楚,可以再講多次嗎？")

                self.FindProduct(c=c+1)

            else:

                self.SOUND.ThreadPlaySound("Note-1")

                self.SPEAK.ThreadSpeak(text="唔好意思,都係聽唔清楚, 請稍後再試")

        else:

            delimiters = ["仲有", "同埋", "和", "加"]
            
            for delimiter in delimiters:
                
                if( delimiter in Text):
                	
                    Text = " ".join(Text.split(delimiter))
            
            result = Text.split()

            print(result)

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

                            self.SPEAK.ThreadSpeak(f"好,成功將物品更改為{RECOMAND_LIST[product_name][0]}")

                            
                        else:

                            self.SOUND.ThreadPlaySound("Note-1")

                            self.SPEAK.ThreadSpeak(f"冇問題, 維持原本物品{product_name}")

                    ProductList.append(product_name)

                else:

                    self.SOUND.ThreadPlaySound("Error")

                    self.SPEAK.ThreadSpeak(f"目標商品{product_name}不存在")

            if(len(ProductList) == 0):

                return

            

            for product in ProductList:

                self.TARGET_PRODUCTS.append(product)

            Products_Text = self.GetProductString(self.TARGET_PRODUCTS)

            self.SOUND.ThreadPlaySound("Note-1")

            self.SPEAK.ThreadSpeak(f"添加尋找物品{Products_Text} 成功")

            self.SOUND.ThreadPlaySound("Note-1")
            
            return self.TARGET_PRODUCTS


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
            
            if ( self.VOICE.Confirm() ) :
                
                for Product in DEL_PRODUCTS :
                    
                    INDEX = self.TARGET_PRODUCTS.index(Product)
                    
                    self.TARGET_PRODUCTS.pop(INDEX)
                    
                self.SPEAK.ThreadSpeak("成功刪除商品.")
                
                self.SOUND.ThreadPlaySound("Note-1")

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

            self.SPEAK.ThreadSpeak(text = f"搵到目標物品 {Object_Name}")
                            
            self.SOUND.DoneSound()

            return True
        
        return False


        
    def ChooseTargetProducts( self,Count = 1 ):

        if( len(self.FOUND_PRODUCTS) == 1 ):

            self.TARGET_PRODUCT = self.FOUND_PRODUCTS[0]

            self.SOUND.ThreadPlaySound( Type = "Note-1")

            self.SPEAK.Say( text = f"搵到目標商品{self.TARGET_PRODUCT} 喺你前方")

            print(f"搵到{self.TARGET_PRODUCT}")

            return self.TARGET_PRODUCTS
        
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

            UserInput = self.VOICE.StartCantonese()
            
            

            if( UserInput in self.FOUND_PRODUCTS ) : 

                self.TARGET_PRODUCT = UserInput

                return UserInput
            
            else :
                 
                self.ChooseTargetObject(Count+1)
            
        else:

            TEXT = "等我幫你揀啦! 我哋搵咗"

            TEXT += f"{self.FOUND_PRODUCTS[0]} 先啦"

            self.SOUND.ThreadPlaySound( Type = "Note-1")

            self.SPEAK.Say( text = TEXT )

            self.SOUND.ThreadPlaySound( Type = "Note-1")

            self.TARGET_PRODUCT = self.FOUND_PRODUCTS[0]

            return self.TARGET_PRODUCTS

        return False