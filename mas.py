import random
import math

#difine to shokika
Agent_Num=10000 #agent no num
opin_list=[] #agent no opinion
F=[0,1,2] #search no frequency
f_list=[] #agent no search frequency
numnum=0 #num for round
shomonai=[] #play no times
Theory=0 #0:group-polarization,1:in-you,2:cognitive-dissonance
P_Filter=1 #Personalize_Filtering,0:nashi,1:ari

shift=0 #0:nashi,1:ari
zero_opin=0 #for decide shift
lk=3 #filtering no tsuyosa ,1:weak - 3:strong
theta=0 #filtering no shikii-chi

fio=open("test.txt","w")

def initial():
    print("Agent_Num..",Agent_Num)
    print("   Theory..",Theory)
    print(" P_Filter..",P_Filter)
    if Theory==0:
        print("    Shift..",shift)

    for i in range(Agent_Num):
        num=random.normalvariate(0.0,3.0)
        numnum=round(num)
        opin_list.append(numnum)

        search_frequency=random.choice(F)
        f_list.append(search_frequency)

        shomonai.append(0)

#        print('{:.2f} '.format(numnum))
#        if i%10==0 and i!=0:
#            print('\n',i)
        """
        if search_frequency==0.25:
            c1+=1
        if search_frequency==0.50:
            c2+=1
        if search_frequency==0.75:
            c3+=1
        """
        fio.write('{:.2f}\n'.format(numnum))
        
    print("\nuser opinion_list num ...",len(opin_list))

    for i in range(21):
        print(" ",i-10,"=...",opin_list.count(i-10))

#    fo.close()


def explore():
#    print(f_list)
#    print(shomonai)
    p1,p2,p3=0,0,0
    avrge,sd=0,0

    for k in range(20):
        print("\nloop...",k+1)

        for i in range(Agent_Num):
            avrge+=opin_list[i]

        print(avrge)
        avrge/=Agent_Num
        print(avrge)
        for i in range(Agent_Num):
            sd+=pow((opin_list[i]-avrge),2)
            """
            if avrge>=0:
                sd+=pow((opin_list[i]-avrge),2)
            else:
                sd+=pow((opin_list[i]+avrge),2)
            """

        print("sd...",sd/Agent_Num)
        sd=math.sqrt(sd/Agent_Num)
        print("Hyojung hensa..",sd)

        for i in range(Agent_Num):
            shomonai[i]+=1
        
            if f_list[i]<1: #25%
                if shomonai[i]%4==0:
                    p1+=1
                    shomonai[i]=0
                    changeopinion(i,avrge,sd)
#                    print("play...0..loop",k)
            if f_list[i]<2 and f_list[i]>0: #50%
                if shomonai[i]%2==0:
                    p2+=1
                    shomonai[i]=0
                    changeopinion(i,avrge,sd)
#                    print("play...1..loop",k)
            if f_list[i]>1 : #75%
                if shomonai[i]%4!=0:
                    p3+=1
                    changeopinion(i,avrge,sd)
#                    print("play...2..loop",k)
        
        if (k+1)%5==0 and (k+1)!=20:
            for j in range(Agent_Num):
                num=opin_list[j]
                numnum=round(num)
                opin_list[j]=numnum

            for j in range(21):
                print(" ",j-10,"=...",opin_list.count(j-10))
                        
#        print(f_list)
#        print(shomonai)
    for i in range(Agent_Num):
        num=opin_list[i]
        numnum=round(num)
        opin_list[i]=numnum
        
    for i in range(21):
        print(" ",i-10,"=...",opin_list.count(i-10))

    print("\n\n0.25...",p1,"0.50...",p2,"0.75...",p3)


#calculate discrepancy 
def calc_discrepancy(a,b):
    discrepancy=0
    discrepancy=abs(a-b)
    return discrepancy


#calculate discrepancy in-you
def calc_dis_crepancy(a,b,type):
    if type==0:
        discrepancy=abs(a-b)
        return discrepancy
    else:
        discrepancy=abs(a+b)
        return discrepancy


def makeopinion(a,b,c):
    sav=0
    zero_opin=0
    cnt_opin=0
    cnt_loop=c
    for i in range(cnt_loop):
        num=random.normalvariate(a,b)
        if P_Filter==0:
            numnum=round(num)
            sav+=numnum
            cnt_opin+=1
        else:
            if a>=0:
                if num>=theta:
                    numnum=round(num)
                    sav+=numnum
                    cnt_opin+=1
            else:
                if num<=theta:
                    numnum=round(num)
                    sav+=numnum
                    cnt_opin+=1

        if i==0:
            zero_opin=sav

        if cnt_opin!=10:
            cnt_loop+=1

    sav=sav/c
    return sav
           

def changeopinion(a,b,c):
    sav=0
    pdunum=10
    high=10 #max value
    low=-10 #minimum value

    if P_Filter==0:
        sav=makeopinion(b,c,pdunum)
    else:
        if opin_list[a]>=0:
            theta=opin_list[a]-(c/lk)
        else:
            theta=opin_list[a]+(c/lk)
        #print("theta..",theta)
        sav=makeopinion(opin_list[a],c,pdunum)
        
    if Theory==0:
        k=0.5 #opinion no henkaryo non-shift
        ka=0.9 #k=a 0.9 or 0.6(weak)
        kb=0.1 #k=b 0.1 or 0.4(weak)
        shift_type=3 #1:risky,2:cautious,3:nashi
        delta=2 #border of filtering ari or nashi

        if shift==0:
            shift_type=3
        else:
            if opin_list[a]==0:
                shift_type=3
            elif opin_list[a]>0:
                if zero_opin>=delta:
                    shift_type=1
                elif zero_opin<=(delta*-1):
                    shift_type=2
                else:
                    shift_type=3
            elif opin_list[a]<0:
                if zero_opin<=(delta*-1):
                    shift_type=1
                elif zero_opin>=delta:
                    shift_type=2
                else:
                    shift_type=3

        if shift_type==3:
            opin_list[a]=k*(sav-opin_list[a])
            """
            if opin_list[a]>=0:
                opin_list[a]=k*(sav-opin_list[a])
            else:
                opin_list[a]=k*(sav+opin_list[a])
            """
        elif shift_type==2: #cautious
            if ((sav>opin_list[a])and(opin_list[a]>0)) or ((sav<opin_list[a])and(opin_list[a]<0)):
                opin_list[a]=kb*(sav-opin_list[a])
                """
                if opin_list[a]>=0:
                    opin_list[a]=kb*(sav-opin_list[a])
                else:
                    opin_list[a]=kb*(sav+opin_list[a])
                """
            elif ((sav<opin_list[a])and(opin_list[a]>0)) or ((sav>opin_list[a])and(opin_list[a]<0)):
                opin_list[a]=ka*(sav-opin_list[a])
                """
                if opin_list[a]>=0:
                    opin_list[a]=ka*(sav-opin_list[a])
                else:
                    opin_list[a]=ka*(sav+opin_list[a])
                """
        else: #risky
            if ((sav>opin_list[a])and(opin_list[a]>0)) or ((sav<opin_list[a])and(opin_list[a]<0)):
                opin_list[a]=ka*(sav-opin_list[a])
                """
                if opin_list[a]>=0:
                    opin_list[a]=ka*(sav-opin_list[a])
                else:
                    opin_list[a]=kb*(sav+opin_list[a])
                """
            elif ((sav<opin_list[a])and(opin_list[a]>0)) or ((sav>opin_list[a])and(opin_list[a]<0)):
                opin_list[a]=kb*(sav-opin_list[a])
                """
                if opin_list[a]>=0:
                    opin_list[a]=kb*(sav-opin_list[a])
                else:
                    opin_list[a]=kb*(sav+opin_list[a])
                """
        """
        if opin_list[a]>=0:
            opin_list[a]=k*(sav-opin_list[a])
        else:
            opin_list[a]=k*(sav+opin_list[a])
        """
    
    if Theory==1:
        opin=0 #henka-ryo
        
        if sav>0:
            if opin_list[a]>0:
                opin=sav-calc_dis_crepancy(opin_list[a],sav,0)
#                opin_list[a]-=(opin/len(opin_list))
                opin_list[a]-=(opin/pdunum)
            elif opin_list[a]<0:
                opin=sav-calc_dis_crepancy(abs(opin_list[a]),sav,0)
#                opin_list[a]+=(opin/len(opin_list))
                opin_list[a]+=(opin/pdunum)
            #kenzai opin==0 nomove            
            #        elif abs(list[i]-persuasion)<3:
            #            list[i]+=(opin/len(list))   
        if sav<0:
            if opin_list[a]>0:
                opin=sav+calc_dis_crepancy(opin_list[a],sav,1)
#                opin_list[a]+=(opin/len(opin_list))
                opin_list[a]+=(opin/pdunum)
            elif opin_list[a]<0:
                opin=sav+calc_dis_crepancy(abs(opin_list[a]),sav,1)
#                opin_list[a]-=(opin/len(opin_list))
                opin_list[a]-=(opin/pdunum)
            #kenzai opin==0 nomove
            #        elif abs(list[i]+persuasion)<3:
            #            list[i]-=(opin/len(list))
        
    #    elif persuasion==high or persuasion==low:

    
    if Theory==2:
        turn=2 #aru ten

        if sav>0:
            if calc_discrepancy(opin_list[a],sav)<=turn:
#                opin_list[a]+=(calc_discrepancy(opin_list[a],sav)/len(opin_list))
                opin_list[a]+=(calc_discrepancy(opin_list[a],sav)/pdunum)
            elif calc_discrepancy(opin_list[a],sav)>turn*2:
#                opin_list[a]-=(abs(calc_discrepancy(opin_list[a],sav)-turn*2))/len(opin_list)
                opin_list[a]-=((abs(calc_discrepancy(opin_list[a],sav)-turn*2))/pdunum)
            elif calc_discrepancy(opin_list[a],sav)>turn and calc_discrepancy(opin_list[a],sav)<turn*2:
#                opin_list[a]+=(abs(calc_discrepancy(opin_list[a],sav)-turn*2))/len(opin_list)
                opin_list[a]+=((abs(calc_discrepancy(opin_list[a],sav)-turn*2))/pdunum)
            """
            else:
                opin_list[0]+=(calc_discrepancy(persuasion,turn)/len(opin_list))
                opin_list[0]-=(calc_discrepancy(opin_list[0],))
            """
        if sav<0:
            if calc_discrepancy(opin_list[a],sav)<=turn:
#                opin_list[a]-=(calc_discrepancy(opin_list[a],sav)/len(opin_list))
                opin_list[a]-=(calc_discrepancy(opin_list[a],sav)/pdunum)
            elif calc_discrepancy(opin_list[a],sav)>turn*2:
#                opin_list[a]+=(abs(calc_discrepancy(opin_list[a],sav)-turn*2))/len(opin_list)
                opin_list[a]+=((abs(calc_discrepancy(opin_list[a],sav)-turn*2))/pdunum)
            elif calc_discrepancy(opin_list[a],sav)>turn and calc_discrepancy(opin_list[a],sav)<turn*2:
#                opin_list[a]-=(abs(calc_discrepancy(opin_list[a],sav)-turn*2))/len(opin_list)
                opin_list[a]-=((abs(calc_discrepancy(opin_list[a],sav)-turn*2))/pdunum)


    if opin_list[a]>high:
        opin_list[a]=high
    if opin_list[a]<low:
        opin_list[a]=low



def main():
#    fo=open("test.txt","w")
    initial()
    explore()
    fio.close()


main()