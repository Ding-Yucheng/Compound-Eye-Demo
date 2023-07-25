clc;
N = ((1:100)*2-1)';

SumN_4 = (2+N)/2.*((N-2)/(2)+1)*2-N;
SumN_6 = (2+N)/2.*((N-2)/1+1)*2-N;

FoVsingle = 22.6;

dFoV = 11.3;
FoV1 = 2*(dFoV*(N-1)/2+FoVsingle/2);

dFoV = 11;
FoV2 = 2*(dFoV*(N-1)/2+FoVsingle/2);

dFoV = 10;
FoV3 = 2*(dFoV*(N-1)/2+FoVsingle/2);

dFoV = 9;
FoV4 = 2*(dFoV*(N-1)/2+FoVsingle/2);

dFoV = 7;
FoV5 = 2*(dFoV*(N-1)/2+FoVsingle/2);

dFoV = 5;
FoV6 = 2*(dFoV*(N-1)/2+FoVsingle/2);

dFoV = 3;
FoV7 = 2*(dFoV*(N-1)/2+FoVsingle/2);

dFoV = 1;
FoV8 = 2*(dFoV*(N-1)/2+FoVsingle/2);

figure;
plot(SumN_6,FoV1,'--rs');
hold on;
plot(SumN_6,FoV2,'--gs');
hold on;
plot(SumN_6,FoV3,'--bs');
hold on;
plot(SumN_6,FoV4,'--ys');
hold on;
plot(SumN_6,FoV5,'--gs');
hold on;
plot(SumN_6,FoV6,'--bs');
hold on;
plot(SumN_6,FoV7,'--bs');
hold on;
plot(SumN_6,FoV8,'--bs');
hold on;
legend('11.3','11','10','9','7','5','3','1');
axis([0,1000,0,220]);

D = [SumN_6,FoV1,FoV2,FoV3,FoV4,FoV5,FoV6,FoV7,FoV8];
xlswrite('hex_Npixel_FoV.xlsx',D);

