<!-- challenge no1 
2 consumer kese run kare  ge aik micro service example order aur address topic producer and consumer 

solution:
    seperate consumer ka use karke run kare ge



challenge no2 
order items pehle add hoge ya phr order 
ye hai ke order items mein order aik fk hai lekin order to bad mein create hoga pehle orderitems create hoge 

challenge no 2 solution 

1. order ka object create kare ge aur usko session main add karde ge.

2. order items create hogi aur unko session mein add karede commit nahi kare ge. 




Final Solution
order items ko is waqat remove karde kiyu ke ye complex example hogi.
sir order ka schema banaye  -->


payment service -> order service
for example payment status completed order-sevice listen and then update orderpament status is paid 
payment service payment status complete hone par aik event producer kare gi thne 
order service us payment ke event ko consumer karega aur apne database mein order pament status ko update kar ga