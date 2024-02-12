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
data_sets = {'\100', '\133', '\var'};

for ii = 1:length(data_sets)

    %Goes into the individual tests directory  then folder
    d = dir(strcat(data_dir, data_sets{1}));
    data_folder = d.folder;

    for jj = 3:length(d)
        if (ii == 1 && jj == 3)
            jawn =1;
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



        end

    end
end
