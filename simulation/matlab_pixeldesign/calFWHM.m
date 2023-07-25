function FWHMcal = calFWHM(x,y)

ymax = max(y);
Halfymax = ymax/2;
temp = -abs(y-Halfymax);
[pks,locs] = findpeaks(temp,x);
if length(locs)<=2
FWHMcal = abs(max(locs)-min(locs));
end
end