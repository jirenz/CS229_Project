%XD = [10, 50, 500, 1000, 2000, 4000, 20000, 40000]
%YD = [2, 67, 75, 71, 78, 73, 75, 76]
%XL = [500, 1000, 2000, 4000, 12000, 20000, 40000]
%YL = [52, 62, 78, 69, 81, 76, 77]
clear
%X = [10, 20, 50, 200, 500, 1000, 2000, 4000, 12000, 20000, 40000]
%YD = [2, 50, 67, 81, 75, 71, 78, 73, 74, 75, 76]
%YL = [1, 5, 9, 59, 52, 62, 78, 69, 81, 76, 77]
1, 5, 10, 20, 50 
20, 100, 200, 400, 1000
XQ = [1, 2, 10, 20, 50]
XQ1 = [41, 60, 64, 65, 40]
XQ2 = [52, 49, 50, 59, 50]
%YQ = [0, 62, 50, 0, 55]
%models/ql_sp_relative_50.t trade 100 2 => 50
%models/ql_sp_relative_20.t trade 100 2 => 62
%models/ql_sp_relative_1.t trade 100 2 => 52
%models/ql_sp_relative_5.t trade 100 2 => 49
%models/ql_sp_relative_10.t trade 100 2 => 50
%models/ql_sp_relative_20.t trade 100 2 => 55
%models/ql_fs_resource_1.t trade 100 2 => 41
%models/ql_fs_resource_5.t trade 100 2 => 60
%models/ql_fs_resource_10.t trade 100 2 => 64
%models/ql_fs_resource_20.t trade 100 2 => 65
%models/ql_fs_resource_50_2.t trade 100 2 => 40

figure
hold on
plot(XQ1,'-s',...
     'color', [1, 1, 0],...
    'LineWidth',3,...
    'MarkerSize',13,...
    'MarkerEdgeColor',[1, 1, 0],...
    'MarkerFaceColor',[1,1,0])
plot(XQ2,'-s',...
     'color', [0, 1, 1],...
    'LineWidth',3,...
    'MarkerSize',13,...
    'MarkerEdgeColor',[0, 1, 1],...
    'MarkerFaceColor',[0,1,1])
%plot(XQ, XQ1, 'color', [1, 0, 1], 'LineWidth',3)
%plot(XQ, XQ2, 'color', [0, 1, 1], 'LineWidth',3)
%plot(YQ, 'color', [0, 0, 1])
set(gca, 'ylim', [30, 70])
set(gca, 'XTick', 1:length(XQ))
set(gca,'XTickLabel', XQ)
set(gca, 'YGrid', 'on')
pos = get(gcf, 'Position'); %// gives x left, y bottom, width, height
width = pos(3);
height = pos(4);
set(gcf, 'Position', [100, 80, width, height * 0.8])

title('Learning curve of q-learner')
xlabel('Training epochs')
ylabel('Winning rate')
rez=1200; %resolution (dpi) of final graphic
f=gcf; %f is the handle of the figure you want to export
figpos=getpixelposition(f); %dont need to change anything here
resolution=get(0,'ScreenPixelsPerInch'); %dont need to change anything here
set(f,'paperunits','inches','papersize',figpos(3:4)/resolution,'paperposition',[0 0 figpos(3:4)/resolution]); %dont need to change anything here
path=''; %the folder where you want to put the file
name='Learning_curve_q_learner.png'; %what you want the file to be called
print(f,fullfile(path,name),'-dpng',['-r',num2str(rez)],'-opengl') %save file 