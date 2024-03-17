%Housekeeping
clear;
clc;
close all;

%Gives current folder path
curr_folder = pwd;

%Goes into the testing data
folder_name = '\Onland_Testing_Data';
data_dir = strcat(pwd, folder_name);


% Onland_Test = dir(data_dir);

%The only data sets we are looking at
data_sets = {'\100', '\133', '\var', '\75'};
% data_sets = {'\test'};


for ii = 1:length(data_sets)

    %Goes into the individual tests directory  then folder
    d = dir(strcat(data_dir, data_sets{ii}));
    data_folder = d.folder;

    for jj = 3:length(d)
        if (ii == 1 && jj == 3)
            jawn = 1;
        else

            %Goes into the trial and takes data
            filename = fullfile(data_folder, d(jj).name);
            data = readmatrix(filename);

            %Seperating each individual activation per sensor
            data1_indicies = find(data(:,2) == 1);
            data1_time = data(data1_indicies, 1);

            data2_indicies = find(data(:,2) == 2);
            data2_time = data(data2_indicies, 1);

            data3_indicies = find(data(:,2) == 3);
            data3_time = data(data3_indicies, 1);

            data_times = {data1_time, data2_time, data3_time};

            RPM1 = [];
            RPM2 = [];
            RPM3 = [];
 
            RPM = {RPM1, RPM2, RPM3};

            %Iterating through calculating RPM over 10 activations
            for kk = 1:length(data_times)
    
                for ll = 10:length(data_times{kk})
                    RPM{kk}(ll - 9) = 10*(60/(data_times{kk}(ll) - data_times{kk}(ll-9)));
                end
            end


            figure()
            hold on
            plot(data1_time(10:end), RPM{1})
            plot(data2_time(10:end), RPM{2})
            plot(data3_time(10:end), RPM{3})
            ylabel('RPM')
            title(d(jj).name)
            %legend('Sensor 1', 'Sensor 2', 'Sensor 3')
            legend('Sprocket1 Sensor', 'Sprocket2 Sensor', 'Prop Sensor')

            hold off


        end

    end
end
