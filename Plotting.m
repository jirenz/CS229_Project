%XD = [10, 50, 500, 1000, 2000, 4000, 20000, 40000]
%YD = [2, 67, 75, 71, 78, 73, 75, 76]
%XL = [500, 1000, 2000, 4000, 12000, 20000, 40000]
%YL = [52, 62, 78, 69, 81, 76, 77]
clear
X = [10, 20, 50, 200, 500, 1000, 2000, 4000, 12000, 20000, 40000]
YD = [2, 50, 67, 81, 75, 71, 78, 73, 74, 75, 76]
YL = [1, 5, 9, 59, 52, 62, 78, 69, 81, 76, 77]
%XQ = [500]
%YQ = [0, 62, 50, 0, 55]
hold on
plot(YD, 'color', [1, 0, 0], 'LineWidth',3)
plot(YL, 'color', [0, 1, 0], 'LineWidth',3)
%plot(YQ, 'color', [0, 0, 1])
set(gca, 'XTick', 1:length(X))
set(gca,'XTickLabel', X)
%
xlabel('Training set data size')
ylabel('Winning rate')
rez=1200; %resolution (dpi) of final graphic
f=gcf; %f is the handle of the figure you want to export
figpos=getpixelposition(f); %dont need to change anything here
resolution=get(0,'ScreenPixelsPerInch'); %dont need to change anything here
set(f,'paperunits','inches','papersize',figpos(3:4)/resolution,'paperposition',[0 0 figpos(3:4)/resolution]); %dont need to change anything here
path=''; %the folder where you want to put the file
name='Learning_curve_supervised.png'; %what you want the file to be called
print(f,fullfile(path,name),'-dpng',['-r',num2str(rez)],'-opengl') %save file 