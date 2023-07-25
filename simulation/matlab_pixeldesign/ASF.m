clc;

D = 1e-3;
L = 5e-3;
FoVs = atan(D/L);
N = 1000;
theta = linspace(-pi/4,pi/4,N)';

AS = exp(-4*log(2)*(theta./FoVs).^2);
FWHM = calFWHM(theta/pi*180,AS);
output = [theta/pi*180,AS];
%xlswrite('ASF.xlsx',output);

figure;
plot(theta/pi*180,AS);