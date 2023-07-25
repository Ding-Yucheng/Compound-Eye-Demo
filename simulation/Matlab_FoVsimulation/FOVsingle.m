clc;
D = xlsread('test.xlsx');
N = 101;

angle = D(51:151,1);
Ipos = D(51:151,2);
Ifull = D(51:151,3);

Ipos = Ipos/2+0.5;
%tempIpos = [Ipos(51:101);Ipos(1:50)];
tempIpos = (cos((1:N)/N*2*pi)'+1)/2;
calIpos = (tempIpos+Ipos);

figure;
plot(angle,Ipos);
hold on;
plot(angle,Ifull);
hold on;
plot(angle,tempIpos);
hold on;
plot(angle,calIpos);

d = 3e-3;
h = 5e-3;
dangle = 20;
anglesingle = (-22:0.1:22)'/180*pi;
%anglesingle = linspace(-atan(d/h),atan(d/h),1000)';
%anglesweep = linspace(-pi/4,pi/4,1000);
r = d/2;
d1 = d/2-h*abs(tan(anglesingle));
d2 = sqrt(r.^2-d1.^2);
dS = pi*r^2/pi*acos(d1/r)-d1.*d2;
FoVsingle1 = (1-dS/(pi*r^2)).*(abs(anglesingle)<=atan(d/h));
%{
figure;
plot(anglesingle,d1);
hold on;
plot(anglesingle,d2);
figure;
plot(anglesingle,dS);
%}
d1 = (d/2-abs(h*tan(anglesingle-dangle/180*pi)));
d2 = sqrt(r.^2-d1.^2);
dS = pi*r^2/pi*acos(d1/r)-d1.*d2;
%FoVsingle2 = dS/(pi*r^2).*((abs(anglesingle-dangle/180*pi))<=atan(d/h));
FoVsingle2 = (1-dS/(pi*r^2)).*((abs(anglesingle-dangle/180*pi))<=atan(d/h));

d1 = (d/2-abs(h*tan(anglesingle+dangle/180*pi)));
d2 = sqrt(r.^2-d1.^2);
dS = pi*r^2/pi*acos(d1/r)-d1.*d2;
%FoVsingle3 = dS/(pi*r^2).*((abs(anglesingle+dangle/180*pi))<=atan(d/h));
FoVsingle3 = (1-dS/(pi*r^2)).*((abs(anglesingle+dangle/180*pi))<=atan(d/h));

FoVmulti = (FoVsingle1+FoVsingle2+FoVsingle3);
%FoVmulti = (FoVmulti-min(FoVmulti))./(max(FoVmulti)-min(FoVmulti))/3;


figure;
plot(anglesingle/pi*180,FoVsingle1,'--rs');
hold on;
plot(anglesingle/pi*180,FoVsingle2,'--gs');
hold on;
plot(anglesingle/pi*180,FoVsingle3,'--bs');
hold on;
plot(anglesingle/pi*180,FoVmulti,'--ys')

D=[anglesingle/pi*180,FoVsingle1,FoVsingle2,FoVsingle3,FoVmulti];
xlswrite('FoV_hd3_5_dangle20.xlsx',D);
