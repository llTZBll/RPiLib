# 说明：PCF8591 模数转换器传感器实验

#####################################################

import PCF8591 as ADC

# 模块地址设置

def makerobo_setup():

 ADC.setup(0x48)  # 设置PCF8591模块地址

# 无限循环

def loop():

  while True:

    print (ADC.read(0)) #读取AIN0的数值，插上跳线帽之后，采用的是内部的电位器；

    ADC.write(ADC.read(0)) # 控制AOUT输出电平控制LED灯

# 异常处理函数
def destroy():

  ADC.write(0) #AOUT输出为0

#程序入口

if __name__ == "__main__":

  try:

    makerobo_setup() #地址设置

    loop()           # 调用无限循环
  except KeyboardInterrupt:
    destroy() #释放AOUT端口