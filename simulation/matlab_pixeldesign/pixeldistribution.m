clc;
r = 15;  %unit mm
FoV = 15/180*pi; %FoV of a single pixel
theta = 9/180*pi;  %polar angle
phai = 10/180*pi;  %azimuthal angle
maxazi = 55/180*pi;
% design 1 2D design
%polar distribution
N = floor(maxazi/theta); %quantity of pixels in polar direction
n = 1:N;
h = r*theta/(FoV-theta); %dead zone distance
%azimuthal distribution
M = 2*pi*sin(n*theta)./phai; % the quantity of pixels at n rings N*theta;

% design 2 hexagon design / pentagon design
interangle = 2*pi/6;
ratio = sin(interangle)/interangle;
%r_hexagon = r*theta/2;
%N_hexagon = (maxazi/(pi/2))*2*pi*r^2/(pi*r_hexagon^2*ratio);

r_tri = r*theta/2;
N_tri = (maxazi/(pi/2))*2*pi*r^2/(r_tri*r_tri/2*sqrt(3)/2)*3/6;