function [] = canalSurface(exercise)
% exercise = 'Swipeleft'
exercise_file = ['data/' exercise 'Data.mat']
hand_file = ['data/' exercise 'ΗandOutput.mat']
upper_file = ['data/' exercise 'UpperOutput.mat']
lower_file = ['data/' exercise 'LowerOutput.mat']
sd = load(exercise_file)
%sd = load('data/SwiperightData.mat'); %load 'sd'
sd = sd.('data');
sd = sd';
sd(1, :) = []
sd(1, :)    
steps = sd(1,:);

max_ = max(steps)
min_ = min(steps)

demoSize = max_;
totalSamples = size(steps, 2);
numDemos = totalSamples/demoSize;

upper_coord = [0, 0, 0];
lower_coord = [0, 0, 0];
hand_coord = [0, 0, 0];

upper_coord_2 = [0, 0, 0];
lower_coord_2 = [0, 0, 0];
hand_coord_2 = [0, 0, 0];

upper_ang = [0, 0, 0];
lower_ang = [0, 0, 0];
hand_ang = [0, 0, 0];

upper_coord_set = {};
lower_coord_set = {};
hand_coord_set = {};

upper_ang_set = {};
lower_ang_set = {};
hand_ang_set = {};

upper_coord_set_2 = {};
lower_coord_set_2 = {};
hand_coord_set_2 = {};

max_distance_upper = -9999*ones(1, max_);
max_distance_upper_2 = -9999*ones(1, max_);
max_distance_lower = -9999*ones(1, max_);
max_distance_lower_2 = -9999*ones(1, max_);
max_distance_hand = -9999*ones(1, max_);
max_distance_hand_2 = -9999*ones(1, max_);

upper_high_x = -9999*ones(1, max_);
upper_high_y = -9999*ones(1, max_);
upper_high_z = -9999*ones(1, max_);
upper_high_x_2 = -9999*ones(1, max_);
upper_high_y_2 = -9999*ones(1, max_);
upper_high_z_2 = -9999*ones(1, max_);
lower_high_x = -9999*ones(1, max_);
lower_high_y = -9999*ones(1, max_);
lower_high_z = -9999*ones(1, max_);
lower_high_x_2 = -9999*ones(1, max_);
lower_high_y_2 = -9999*ones(1, max_);
lower_high_z_2 = -9999*ones(1, max_);
hand_high_x = -9999*ones(1, max_);
hand_high_y = -9999*ones(1, max_);
hand_high_z = -9999*ones(1, max_);
hand_high_x_2 = -9999*ones(1, max_);
hand_high_y_2 = -9999*ones(1, max_);
hand_high_z_2 = -9999*ones(1, max_);

upper_high_ang_x = -9999*ones(1, max_);
upper_high_ang_y = -9999*ones(1, max_);
upper_high_ang_z = -9999*ones(1, max_);
upper_low_ang_x = 9999*ones(1, max_);
upper_low_ang_y = 9999*ones(1, max_);
upper_low_ang_z = 9999*ones(1, max_);

lower_high_ang_x = -9999*ones(1, max_);
lower_high_ang_y = -9999*ones(1, max_);
lower_high_ang_z = -9999*ones(1, max_);
lower_low_ang_x = 9999*ones(1, max_);
lower_low_ang_y = 9999*ones(1, max_);
lower_low_ang_z = 9999*ones(1, max_);

hand_high_ang_x = -9999*ones(1, max_);
hand_high_ang_y = -9999*ones(1, max_);
hand_high_ang_z = -9999*ones(1, max_);
hand_low_ang_x = 9999*ones(1, max_);
hand_low_ang_y = 9999*ones(1, max_);
hand_low_ang_z = 9999*ones(1, max_);

upper_low_x = 9999*ones(1, max_);
upper_low_y = 9999*ones(1, max_);
upper_low_z = 9999*ones(1, max_);
upper_low_x_2 = 9999*ones(1, max_);
upper_low_y_2 = 9999*ones(1, max_);
upper_low_z_2 = 9999*ones(1, max_);
lower_low_x = 9999*ones(1, max_);
lower_low_y = 9999*ones(1, max_);
lower_low_z = 9999*ones(1, max_);
lower_low_x_2 = 9999*ones(1, max_);
lower_low_y_2 = 9999*ones(1, max_);
lower_low_z_2 = 9999*ones(1, max_);
hand_low_x = 9999*ones(1, max_);
hand_low_y = 9999*ones(1, max_);
hand_low_z = 9999*ones(1, max_);
hand_low_x_2 = 9999*ones(1, max_);
hand_low_y_2 = 9999*ones(1, max_);
hand_low_z_2 = 9999*ones(1, max_);

upper_coord_x = {};
upper_coord_y = {};
upper_coord_z = {};
upper_coord_x_2 = {};
upper_coord_y_2 = {};
upper_coord_z_2 = {};

upper_ang_x = {};
upper_ang_y = {};
upper_ang_z = {};
lower_ang_X = {};
lower_ang_y = {};
lower_ang_z = {};
hand_ang_x = {};
hand_ang_y = {};
hand_ang_z = {};

upper_ang_set = {};
lower_ang_set = {};
hand_ang_set = {};

idx = 1;
for(i = 1:totalSamples)
    idx_ = mod(i, max_);
    if(idx_==0)
        idx_ = max_;
    end
    if(sd(2,i)>upper_high_x(idx_))
        upper_high_x(idx_) = sd(2, i);
    end
    if(sd(2,i)<upper_low_x(idx_))
        upper_low_x(idx_) = sd(2, i);
    end

    if(sd(3,i)>upper_high_y(idx_))
        upper_high_y(idx_) = sd(3, i);
    end
    if(sd(3,i)<upper_low_y(idx_))
        upper_low_y(idx_) = sd(3, i);
    end

    if(sd(4,i)>upper_high_z(idx_))
        upper_high_z(idx_) = sd(4, i);
    end
    if(sd(4,i)<upper_low_z(idx_))
        upper_low_z(idx_) = sd(4, i);
    end
    
    upper_coord = [upper_coord; [sd(2,i), sd(3,i) sd(4,i)]];
    lower_coord = [lower_coord; [sd(9,i), sd(10,i) sd(11,i)]];
    hand_coord = [hand_coord; [sd(16,i), sd(17,i) sd(18,i)]];
    
    upper_ang = [upper_ang; quat2eul([sd(5,i) sd(6,i) sd(7,i) sd(8,i)])];
    lower_ang = [lower_ang; quat2eul([sd(12,i) sd(13,i) sd(14,i) sd(15,i)])];
    hand_ang = [hand_ang; quat2eul([sd(19,i) sd(20,i) sd(21,i) sd(22,i)])];
    i
    %idx_
    %size(upper_ang)
    size(upper_coord)
    %size(upper_high_ang_x)
    %upper_ang(i, 1)
    %upper_high_ang_x(idx_)
    max_
    if(upper_ang(idx_, 1)>upper_high_ang_x(idx_))
        upper_high_ang_x(idx_) = upper_ang(idx_, 1);
    end
    if(upper_ang(idx_, 1)<upper_low_ang_x(idx_))
        upper_low_ang_x(idx_) = upper_ang(idx_, 1);
    end
    if(upper_ang(idx_, 2)>upper_high_ang_y(idx_))
        upper_high_ang_y(idx_) = upper_ang(idx_, 2);
    end
    if(upper_ang(idx_, 2)<upper_low_ang_y(idx_))
        upper_low_ang_y(idx_) = upper_ang(idx_, 2);
    end
    if(upper_ang(idx_, 3)>upper_high_ang_z(idx_))
        upper_high_ang_z(idx_) = upper_ang(idx_, 3);
    end
    if(upper_ang(idx_, 3)<upper_low_ang_z(idx_))
        upper_low_ang_z(idx_) = upper_ang(idx_, 3);
    end
    
    if(lower_ang(idx_, 1)>lower_high_ang_x(idx_))
        lower_high_ang_x(idx_) = lower_ang(idx_, 1);
    end
    if(lower_ang(idx_, 1)<lower_low_ang_x(idx_))
        lower_low_ang_x(idx_) = lower_ang(idx_, 1);
    end
    if(lower_ang(idx_, 2)>lower_high_ang_y(idx_))
        lower_high_ang_y(idx_) = lower_ang(idx_, 2);
    end
    if(lower_ang(idx_, 2)<lower_low_ang_y(idx_))
        lower_low_ang_y(idx_) = lower_ang(idx_, 2);
    end
    if(lower_ang(idx_, 3)>lower_high_ang_z(idx_))
        lower_high_ang_z(idx_) = lower_ang(idx_, 3);
    end
    if(lower_ang(idx_, 3)<lower_low_ang_z(idx_))
        lower_low_ang_z(idx_) = lower_ang(idx_, 3);
    end
    
    if(hand_ang(idx_, 1)>hand_high_ang_x(idx_))
        hand_high_ang_x(idx_) = hand_ang(idx_, 1);
    end
    if(hand_ang(idx_, 1)<hand_low_ang_x(idx_))
        hand_low_ang_x(idx_) = hand_ang(idx_, 1);
    end
    if(hand_ang(idx_, 2)>hand_high_ang_y(idx_));
        hand_high_ang_y(idx_) = hand_ang(idx_, 2);
    end
    if(hand_ang(idx_, 2)<hand_low_ang_y(idx_))
        hand_low_ang_y(idx_) = hand_ang(idx_, 2);
    end
    if(hand_ang(idx_, 3)>hand_high_ang_z(idx_))
        hand_high_ang_z(idx_) = hand_ang(idx_, 3);
    end
    if(hand_ang(idx_, 3)<hand_low_ang_z(idx_))
        hand_low_ang_z(idx_) = hand_ang(idx_, 3);
    end
    
    if(sd(1,i)==max_)
        upper_coord(1,:) = [];
        lower_coord(1,:) = [];
        hand_coord(1,:) = [];
        
        upper_ang(1,:) = [];
        lower_ang(1,:) = [];
        hand_ang(1,:) = [];
        
        upper_coord_set_x{idx} = upper_coord(:,1);
        upper_coord_set_y{idx} = upper_coord(:,2);
        upper_coord_set_z{idx} = upper_coord(:,3);
        upper_ang_set_x{idx} = upper_ang(:,1);
        upper_ang_set_y{idx} = upper_ang(:,2);
        upper_ang_set_z{idx} = upper_ang(:,3);
        
        lower_coord_set_x{idx} = lower_coord(:,1);
        lower_coord_set_y{idx} = lower_coord(:,2);
        lower_coord_set_z{idx} = lower_coord(:,3);
        lower_ang_set_x{idx} = lower_ang(:,1);
        lower_ang_set_y{idx} = lower_ang(:,2);
        lower_ang_set_z{idx} = lower_ang(:,3);
        
        hand_coord_set_x{idx} = hand_coord(:,1);
        hand_coord_set_y{idx} = hand_coord(:,2);
        hand_coord_set_z{idx} = hand_coord(:,3);
        hand_ang_set_x{idx} = hand_ang(:,1);
        hand_ang_set_y{idx} = hand_ang(:,2);
        hand_ang_set_z{idx} = hand_ang(:,3);
        
        upper_coord_set{idx} = upper_coord;
        lower_coord_set{idx} = lower_coord;
        hand_coord_set{idx} = hand_coord;
        upper_ang_set{idx} = upper_ang;
        lower_ang_set{idx} = lower_ang;
        hand_ang_set{idx} = hand_ang;
        
        upper_coord =[0, 0, 0];
        lower_coord =[0, 0, 0];
        hand_coord =[0, 0, 0];

        upper_ang =[0, 0, 0];
        lower_ang =[0, 0, 0];
        hand_ang =[0, 0, 0];
        
        idx = idx + 1;
    end
end

for (i=1:numDemos)
    upper_coord_set_x{i} = upper_coord_set{i}(:,1);
    upper_coord_set_y{i} = upper_coord_set{i}(:,2);
    upper_coord_set_z{i} = upper_coord_set{i}(:,3);
    
    temp = upper_coord_set{1, i};
    for(j=1:demoSize);
        r=0.3;
        x = temp(j, 1);
        y = temp(j, 2);
        z = temp(j, 3);
        ax = atan2(sqrt(y^2+z^2),x);
        ay = atan2(sqrt(z^2+x^2),y);
        az = atan2(sqrt(x^2+y^2),z);
        xzy = [2*r*sin(ay)*sin(az), 2*r*sin(ay)*cos(az),  2*r*cos(ay)];

        temp(j,1) = xzy(1);
        temp(j,3) = xzy(2);
        temp(j,2) = xzy(3);

        if(temp(j,1)>upper_high_x_2(i))
           upper_high_x_2(i) = temp(j,1);
        end
        if(temp(j,1)<upper_low_x_2(i))
           upper_low_x_2(i) = temp(j,1);
        end
        if(temp(j,3)>upper_high_z_2(i))
           upper_high_z_2(i) = temp(j,3);
        end
        if(temp(j,3)<upper_low_z_2(i))
            upper_high_y_2(i) = temp(j,2);
        end
        if(temp(j,2)<upper_low_y_2(i))
            upper_low_y_2(i) = temp(j,2);
        end
        if(temp(j,2)>upper_high_y_2(i))
            upper_high_y_2(i) = temp(j,2);
        end
    end
    upper_coord_set_2{i} = temp;
    
    upper_coord_set_x_2{i} = upper_coord_set_2{i}(:,1);
    upper_coord_set_y_2{i} = upper_coord_set_2{i}(:,2);
    upper_coord_set_z_2{i} = upper_coord_set_2{i}(:,3);
    
    prev = upper_coord_set_2{i};
    temp = lower_coord_set{i};
    r=0.3;
    for(j=1:demoSize)
        x = temp(j, 1) + prev(j, 1);
        y = temp(j, 2) + prev(j, 2);
        z = temp(j, 3) + prev(j, 3);
        ax = atan2(sqrt(y^2+z^2),x);
        ay = atan2(sqrt(z^2+x^2),y);
        az = atan2(sqrt(x^2+y^2),z);
        xzy = [2*r*sin(ay)*sin(az), 2*r*sin(ay)*cos(az),  2*r*cos(ay)];
        
        temp(j,1) = temp(j, 1) + xzy(1);
        temp(j,3) = temp(j, 3) + xzy(2);
        temp(j,2) = temp(j, 2) + xzy(3);
        
        if(temp(j,1)>lower_high_x(j))
            lower_high_x(j) = temp(j,1);
        end
        if(temp(j,1)<lower_low_x(j))
            lower_low_x(j) = temp(j,1);
        end
        if(temp(j,3)>lower_high_z(j))
            lower_high_z(j) = temp(j,3);
        end
        if(temp(j,3)<lower_low_z(j))
            lower_low_z(j) = temp(j,3);
        end
        if(temp(j,2)>lower_high_y(j))
            lower_high_y(j) = temp(j,2);
        end
        if(temp(j,2)<lower_low_y(j))
            lower_low_y(j) = temp(j,2);
        end
    end
    lower_coord_set{i} = temp;
    
    lower_coord_set_x{i} = lower_coord_set{i}(:,1);
    lower_coord_set_y{i} = lower_coord_set{i}(:,2);
    lower_coord_set_z{i} = lower_coord_set{i}(:,3);
    
    prev = lower_coord_set{i};
    temp = lower_coord_set{i};
    r=0.3;
    for(j=1:size(temp,1))
        x = temp(j, 1) + prev(j, 1);
        y = temp(j, 2) + prev(j, 2);
        z = temp(j, 3) + prev(j, 3);
        ax = atan2(sqrt(y^2+z^2),x);
        ay = atan2(sqrt(z^2+x^2),y);
        az = atan2(sqrt(x^2+y^2),z);
        xzy = [r*sin(ay)*sin(az), r*sin(ay)*cos(az),  r*cos(ay)];
        
        temp(j,1) = temp(j, 1) + xzy(1);
        temp(j,3) = temp(j, 3) + xzy(2);
        temp(j,2) = temp(j, 2) + xzy(3);
        
        if(temp(j,1)>lower_high_x_2(j))
            lower_high_x_2(j) = temp(j,1);
        end
        if(temp(j,1)<lower_low_x_2(j))
            lower_low_x_2(j) = temp(j,1);
        end
        if(temp(j,3)>lower_high_z_2(j))
            lower_high_z_2(j) = temp(j,3);
        end
        if(temp(j,3)<lower_low_z_2(j))
            lower_low_z_2(j) = temp(j,3);
        end
        if(temp(j,2)>lower_high_y_2(j))
            lower_high_y_2(j) = temp(j,2);
        end
        if(temp(j,2)<lower_low_y_2(j))
            lower_low_y_2(j) = temp(j,2);
        end
    end
    lower_coord_set_2{i} = temp;
    
    lower_coord_set_x_2{i} = lower_coord_set_2{i}(:,1);
    lower_coord_set_y_2{i} = lower_coord_set_2{i}(:,2);
    lower_coord_set_z_2{i} = lower_coord_set_2{i}(:,3);
    
    prev = lower_coord_set_2{i};
    temp = lower_coord_set_2{i};
    r=0.05;
    for(j=1:size(temp,1))
        x = temp(j, 1) + prev(j, 1);
        y = temp(j, 2) + prev(j, 2);
        z = temp(j, 3) + prev(j, 3);
        ax = atan2(sqrt(y^2+z^2),x);
        ay = atan2(sqrt(z^2+x^2),y);
        az = atan2(sqrt(x^2+y^2),z);
        xzy = [r*sin(ay)*sin(az), r*sin(ay)*cos(az),  r*cos(ay)];
        
        temp(j,1) = temp(j, 1) + xzy(1);
        temp(j,3) = temp(j, 3) + xzy(2);
        temp(j,2) = temp(j, 2) + xzy(3);
        
        if(temp(j,1)>hand_high_x(j))
            hand_high_x(j) = temp(j,1);
        end
        if(temp(j,1)<hand_low_x(j))
            hand_low_x(j) = temp(j,1);
        end
        if(temp(j,3)>hand_high_z(j))
            hand_high_z(j) = temp(j,3);
        end
        if(temp(j,3)<hand_low_z(j))
            hand_low_z(j) = temp(j,3);
        end
        if(temp(j,2)>hand_high_y(j))
            hand_high_y(j) = temp(j,2);
        end
        if(temp(j,2)<hand_low_y(j))
            hand_low_y(j) = temp(j,2);
        end
    end
    hand_coord_set{i} = temp;
    
    hand_coord_set_x{i} = hand_coord_set{i}(:,1);
    hand_coord_set_y{i} = hand_coord_set{i}(:,2);
    hand_coord_set_z{i} = hand_coord_set{i}(:,3);
    
    prev = hand_coord_set{i};
    temp = hand_coord_set{i};
    r=0.05;
    for(j=1:size(temp,1))
        x = temp(j, 1) + prev(j, 1);
        y = temp(j, 2) + prev(j, 2);
        z = temp(j, 3) + prev(j, 3);
        ax = atan2(sqrt(y^2+z^2),x);
        ay = atan2(sqrt(z^2+x^2),y);
        az = atan2(sqrt(x^2+y^2),z);
        xzy = [r*sin(ay)*sin(az), r*sin(ay)*cos(az),  r*cos(ay)];
        
        temp(j,1) = temp(j, 1) + xzy(1);
        temp(j,3) = temp(j, 3) + xzy(2);
        temp(j,2) = temp(j, 2) + xzy(3);
        
        if(temp(j,1)>hand_high_x_2(j))
            hand_high_x_2(j) = temp(j,1);
        end
        if(temp(j,1)<hand_low_x_2(j))
            hand_low_x_2(j) = temp(j,1);
        end
        if(temp(j,3)>hand_high_z_2(j))
            hand_high_z_2(j) = temp(j,3);
        end
        if(temp(j,3)<hand_low_z_2(j))
            hand_low_z_2(j) = temp(j,3);
        end
        if(temp(j,2)>hand_high_y_2(j))
            hand_high_y_2(j) = temp(j,2);
        end
        if(temp(j,2)<hand_low_y_2(j))
            hand_low_y_2(j) = temp(j,2);
        end
    end
    hand_coord_set_2{i} = temp;
    
    hand_coord_set_x_2{i} = hand_coord_set_2{i}(:,1);
    hand_coord_set_y_2{i} = hand_coord_set_2{i}(:,2);
    hand_coord_set_z_2{i} = hand_coord_set_2{i}(:,3);
end

mean_upper_coord = zeros(size(upper_coord_set{1}));
mean_lower_coord = zeros(size(upper_coord_set{1}));
mean_hand_coord = zeros(size(upper_coord_set{1}));

mean_upper_coord_2 = zeros(size(upper_coord_set_2{1}));
mean_lower_coord_2 = zeros(size(upper_coord_set_2{1}));
mean_hand_coord_2 = zeros(size(upper_coord_set_2{1}));

mean_upper_ang = zeros(size(upper_ang_set{1}));
mean_lower_ang = zeros(size(upper_ang_set{1}));
mean_hand_ang = zeros(size(upper_ang_set{1}));

mean_upper_ang_x = zeros(size(upper_ang_set_x{1}));
mean_upper_ang_y = zeros(size(upper_ang_set_y{1}));
mean_upper_ang_z = zeros(size(upper_ang_set_z{1}));

mean_lower_ang_x = zeros(size(lower_ang_set_x{1}));
mean_lower_ang_y = zeros(size(lower_ang_set_y{1}));
mean_lower_ang_z = zeros(size(lower_ang_set_z{1}));

mean_hand_ang_x = zeros(size(hand_ang_set_x{1}));
mean_hand_ang_y = zeros(size(hand_ang_set_y{1}));
mean_hand_ang_z = zeros(size(hand_ang_set_z{1}));

mean_upper_coord_x = zeros(size(upper_coord_set_x{1}));
mean_upper_coord_y = zeros(size(upper_coord_set_y{1}));
mean_upper_coord_z = zeros(size(upper_coord_set_z{1}));
mean_lower_coord_x = zeros(size(upper_coord_set_x{1}));
mean_lower_coord_y = zeros(size(upper_coord_set_y{1}));
mean_lower_coord_z = zeros(size(upper_coord_set_z{1}));
mean_hand_coord_x = zeros(size(upper_coord_set_x{1}));
mean_hand_coord_y = zeros(size(upper_coord_set_y{1}));
mean_hand_coord_z = zeros(size(upper_coord_set_z{1}));

mean_upper_coord_x_2 = zeros(size(upper_coord_set_x_2{1}));
mean_upper_coord_y_2 = zeros(size(upper_coord_set_y_2{1}));
mean_upper_coord_z_2 = zeros(size(upper_coord_set_z_2{1}));
mean_lower_coord_x_2 = zeros(size(upper_coord_set_x_2{1}));
mean_lower_coord_y_2 = zeros(size(upper_coord_set_y_2{1}));
mean_lower_coord_z_2 = zeros(size(upper_coord_set_z_2{1}));
mean_hand_coord_x_2 = zeros(size(upper_coord_set_x_2{1}));
mean_hand_coord_y_2 = zeros(size(upper_coord_set_y_2{1}));
mean_hand_coord_z_2 = zeros(size(upper_coord_set_z_2{1}));

for i=1:numDemos
    mean_upper_coord = mean_upper_coord+upper_coord_set{i};
    mean_upper_coord_2 = mean_upper_coord_2+upper_coord_set_2{i};
    mean_lower_coord = mean_lower_coord+lower_coord_set{i};
    mean_lower_coord_2 = mean_lower_coord_2+lower_coord_set_2{i};
    mean_hand_coord = mean_hand_coord+hand_coord_set{i};
    mean_hand_coord_2 = mean_hand_coord_2+hand_coord_set_2{i};
    
    mean_upper_coord_x = mean_upper_coord_x + upper_coord_set_x{i};
    mean_upper_coord_y = mean_upper_coord_y + upper_coord_set_y{i};
    mean_upper_coord_z = mean_upper_coord_z + upper_coord_set_z{i};
    mean_upper_coord_x_2 = mean_upper_coord_x_2 + upper_coord_set_x_2{i};
    mean_upper_coord_y_2 = mean_upper_coord_y_2 + upper_coord_set_y_2{i};
    mean_upper_coord_z_2 = mean_upper_coord_z_2 + upper_coord_set_z_2{i};
    
    mean_lower_coord_x = mean_lower_coord_x + lower_coord_set_x{i};
    mean_lower_coord_y = mean_lower_coord_y + lower_coord_set_y{i};
    mean_lower_coord_z = mean_lower_coord_z + lower_coord_set_z{i};
    mean_lower_coord_x_2 = mean_lower_coord_x_2 + lower_coord_set_x_2{i};
    mean_lower_coord_y_2 = mean_lower_coord_y_2 + lower_coord_set_y_2{i};
    mean_lower_coord_z_2 = mean_lower_coord_z_2 + lower_coord_set_z_2{i};
    
    mean_hand_coord_x = mean_hand_coord_x + hand_coord_set_x{i};
    mean_hand_coord_y = mean_hand_coord_y + hand_coord_set_y{i};
    mean_hand_coord_z = mean_hand_coord_z + hand_coord_set_z{i};
    mean_hand_coord_x_2 = mean_hand_coord_x_2 + hand_coord_set_x_2{i};
    mean_hand_coord_y_2 = mean_hand_coord_y_2 + hand_coord_set_y_2{i};
    mean_hand_coord_z_2 = mean_hand_coord_z_2 + hand_coord_set_z_2{i};
    
    mean_upper_ang = mean_upper_ang + upper_ang_set{i};
    mean_upper_ang_x = mean_upper_ang_x + upper_ang_set_x{i};
    mean_upper_ang_y = mean_upper_ang_y + upper_ang_set_y{i};
    mean_upper_ang_z = mean_upper_ang_z + upper_ang_set_z{i};
    
    mean_lower_ang = mean_lower_ang + lower_ang_set{i};
    mean_lower_ang_x = mean_lower_ang_x + lower_ang_set_x{i};
    mean_lower_ang_y = mean_lower_ang_y + lower_ang_set_y{i};
    mean_lower_ang_z = mean_lower_ang_z + lower_ang_set_z{i};
    
    mean_hand_ang = mean_hand_ang + hand_ang_set{i};
    mean_hand_ang_x = mean_hand_ang_x + hand_ang_set_x{i};
    mean_hand_ang_y = mean_hand_ang_y + hand_ang_set_y{i};
    mean_hand_ang_z = mean_hand_ang_z + hand_ang_set_z{i};
end

mean_upper_coord = mean_upper_coord/numDemos;
mean_upper_coord_2 = mean_upper_coord_2/numDemos;
mean_lower_coord = mean_lower_coord/numDemos;
mean_lower_coord_2 = mean_lower_coord_2/numDemos;
mean_hand_coord = mean_hand_coord/numDemos;
mean_hand_coord_2 = mean_hand_coord_2/numDemos;

mean_upper_coord_x = mean_upper_coord_x/numDemos;
mean_upper_coord_y = mean_upper_coord_y/numDemos;
mean_upper_coord_z = mean_upper_coord_z/numDemos;
mean_upper_coord_x_2 = mean_upper_coord_x_2/numDemos;
mean_upper_coord_y_2 = mean_upper_coord_y_2/numDemos;
mean_upper_coord_z_2 = mean_upper_coord_z_2/numDemos;

mean_lower_coord_x = mean_lower_coord_x/numDemos;
mean_lower_coord_y = mean_lower_coord_y/numDemos;
mean_lower_coord_z = mean_lower_coord_z/numDemos;
mean_lower_coord_x_2 = mean_lower_coord_x_2/numDemos;
mean_lower_coord_y_2 = mean_lower_coord_y_2/numDemos;
mean_lower_coord_z_2 = mean_lower_coord_z_2/numDemos;

mean_hand_coord_x = mean_hand_coord_x/numDemos;
mean_hand_coord_z = mean_hand_coord_z/numDemos;
mean_hand_coord_y = mean_hand_coord_y/numDemos;
mean_hand_coord_x_2 = mean_hand_coord_x_2/numDemos;
mean_hand_coord_y_2 = mean_hand_coord_y_2/numDemos;
mean_hand_coord_z_2 = mean_hand_coord_z_2/numDemos;

mean_upper_ang = mean_upper_ang/numDemos;
mean_upper_ang_x = mean_upper_ang_x/numDemos;
mean_upper_ang_y = mean_upper_ang_y/numDemos;
mean_upper_ang_z = mean_upper_ang_z/numDemos;

mean_lower_ang = mean_lower_ang/numDemos;
mean_lower_ang_x = mean_lower_ang_x/numDemos;
mean_lower_ang_y = mean_lower_ang_y/numDemos;
mean_lower_ang_z = mean_lower_ang_z/numDemos;

mean_hand_ang = mean_hand_ang/numDemos;
mean_hand_ang_x = mean_hand_ang_x/numDemos;
mean_hand_ang_y = mean_hand_ang_y/numDemos;
mean_hand_ang_z = mean_hand_ang_z/numDemos;

for(j=1:demoSize)
    for(i=1:numDemos)
        i;
        j;
        upper_coord_set{i}(j, :);
        mean_upper_coord(j, :);
        d = abs(norm(mean_upper_coord(j, :) - upper_coord_set{i}(j, :)));
        if(d>max_distance_upper(j))
            max_distance_upper(j) = d;
        end
        d = abs(norm(mean_upper_coord_2(j, :) - upper_coord_set_2{i}(j, :)));
        if(d>max_distance_upper_2(j))
            max_distance_upper_2(j) = d;
        end
        
        d = abs(norm(mean_lower_coord(j, :) - lower_coord_set{i}(j, :)));
        if(d>max_distance_lower(j))
            max_distance_lower(j) = d;
        end
        d = abs(norm(mean_lower_coord_2(j, :) - lower_coord_set_2{i}(j, :)));
        if(d>max_distance_lower_2(j))
            max_distance_lower_2(j) = d;
        end
        
        d = abs(norm(mean_hand_coord(j, :) - hand_coord_set{i}(j, :)));
        if(d>max_distance_hand(j))
            max_distance_hand(j) = d;
        end
        d = abs(norm(mean_hand_coord_2(j, :) - hand_coord_set_2{i}(j, :)));
        if(d>max_distance_hand_2(j))
            max_distance_hand_2(j) = d;
        end
    end
end


figure
for(i=1:numDemos)
    %plot3(upper_coord_set{i}(:, 1), upper_coord_set{i}(:, 2), upper_coord_set{i}(:, 3), '-*', 'Color', [i/numDemos*0.2, 0 ,0])
    %hold on;
    plot3(upper_coord_set_2{i}(:, 1), upper_coord_set_2{i}(:, 2), upper_coord_set_2{i}(:, 3), '-o', 'Color', [i/numDemos, 0 ,0])
    hold on;
    %plot3(lower_coord_set{i}(:, 1), lower_coord_set{i}(:, 2), lower_coord_set{i}(:, 3), '-*', 'Color', [0, 0 ,i/numDemos*0.2])
    %hold on;
    plot3(lower_coord_set_2{i}(:, 1), lower_coord_set_2{i}(:, 2), lower_coord_set_2{i}(:, 3), '-o', 'Color', [0, 0 ,i/numDemos*0.2])
    hold on;
    %plot3(hand_coord_set{i}(:, 1), hand_coord_set{i}(:, 2), hand_coord_set{i}(:, 3), '-*', 'Color', [0, i/numDemos*0.2, 0])
    %grid on;
    plot3(hand_coord_set_2{i}(:, 1), hand_coord_set_2{i}(:, 2), hand_coord_set_2{i}(:, 3), '-o', 'Color', [0, i/numDemos*0.2, 0])
    grid on
end

%plot3(mean_upper_coord(:,1), mean_upper_coord(:,2), mean_upper_coord(:,3), '-yo')
%hold on;
plot3(mean_upper_coord_2(:,1), mean_upper_coord_2(:,2), mean_upper_coord_2(:,3), '-y*')
hold on;
%plot3(mean_lower_coord(:,1), mean_lower_coord(:,2), mean_lower_coord(:,3), '-yo')
%hold on;
plot3(mean_lower_coord_2(:,1), mean_lower_coord_2(:,2), mean_lower_coord_2(:,3), '-y*')
hold on;
%plot3(mean_hand_coord(:,1), mean_hand_coord(:,2), mean_hand_coord(:,3), '-yo')
%hold on;
plot3(mean_hand_coord_2(:,1), mean_hand_coord_2(:,2), mean_hand_coord_2(:,3), '-y*')
hold on;

sdfhsdh

figure('name','Upper x-y-z')
subplot(3, 2, 1)
for(i=1:numDemos)
    plot(upper_coord_set_x{i}, '-o', 'Color',[i/numDemos, 0, 0]);
    hold on;
end
plot(mean_upper_coord_x, '-xy')
plot(upper_low_x, 'Color', [0, 0, 0])
plot(upper_high_x, 'Color', [0, 0, 0])

subplot(3, 2, 2)
for(i=1:numDemos)
    plot(upper_coord_set_x{i}, upper_coord_set_y{i}, '-o', 'Color',[i/numDemos, 0, 0]);
    hold on;
end
plot(mean_upper_coord_x, mean_upper_coord_y, '-xy')

subplot(3, 2, 3)
for(i=1:numDemos)
    plot(upper_coord_set_y{i}, '-o', 'Color',[0, i/numDemos,  0]);
    hold on;
end
plot(mean_upper_coord_y, '-xy');
plot(upper_low_y, 'Color', [0, 0, 0]);
plot(upper_high_y, 'Color', [0, 0, 0]);

subplot(3, 2, 4)
for(i=1:numDemos)
    plot(upper_coord_set_x{i}, upper_coord_set_z{i}, '-o', 'Color',[0, i/numDemos,  0]);
    hold on;
end
plot(mean_upper_coord_x, mean_upper_coord_z, '-xy');

subplot(3, 2, 5)
for(i=1:numDemos)
    plot(upper_coord_set_z{i}, '-o', 'Color',[0, 0, i/numDemos]);
    hold on;
end
plot(upper_low_z, 'Color', [0, 0, 0]);
plot(upper_high_z, 'Color', [0, 0, 0]);
plot(mean_upper_coord_z, '-xy')

subplot(3, 2, 6)
for(i=1:numDemos)
    plot(upper_coord_set_y{i}, upper_coord_set_z{i},'-o', 'Color',[0, 0, i/numDemos])
    hold on;
end
plot(mean_upper_coord_y, mean_upper_coord_z, '-xy')

figure('name','lower x-y-z')
subplot(3, 2, 1)
for(i=1:numDemos)
    plot(lower_coord_set_x{i}, '-o', 'Color',[i/numDemos, 0, 0])
    hold on;
end
plot(mean_lower_coord_x, '-xy')
plot(lower_low_x, 'Color', [0, 0, 0])
plot(lower_high_x, 'Color', [0, 0, 0])

subplot(3, 2, 2)
for(i=1:numDemos)
    plot(lower_coord_set_x{i}, lower_coord_set_y{i}, '-o', 'Color',[i/numDemos, 0, 0])
    hold on;
end
plot(mean_lower_coord_x, mean_lower_coord_y, '-xy')

subplot(3, 2, 3)
for(i=1:numDemos)
    plot(lower_coord_set_y{i}, '-o', 'Color',[0, i/numDemos,  0])
    hold on;
end
plot(mean_lower_coord_y, '-xy')
plot(lower_low_y, 'Color', [0, 0, 0])
plot(lower_high_y, 'Color', [0, 0, 0])

subplot(3, 2, 4)
for(i=1:numDemos)
    plot(lower_coord_set_x{i}, lower_coord_set_z{i}, '-o', 'Color',[0, i/numDemos,  0])
    hold on;
end
plot(mean_lower_coord_x, mean_lower_coord_z, '-xy')

subplot(3, 2, 5)
for(i=1:numDemos)
    plot(lower_coord_set_z{i}, '-o', 'Color',[0, 0, i/numDemos])
    hold on;
end
plot(mean_lower_coord_z, '-xy')
plot(lower_low_z, 'Color', [0, 0, 0])
plot(lower_high_z, 'Color', [0, 0, 0])

subplot(3, 2, 6)
for(i=1:numDemos)
    plot(lower_coord_set_y{i}, lower_coord_set_z{i},'-o', 'Color',[0, 0, i/numDemos])
    hold on;
end
plot(mean_lower_coord_y, mean_lower_coord_z, '-xy')

figure('name','hand x-y-z')
subplot(3, 2, 1)
for(i=1:numDemos)
    plot(hand_coord_set_x{i}, '-o', 'Color',[i/numDemos, 0, 0])
    hold on;
end
plot(mean_hand_coord_x, '-xy')
plot(hand_low_x, 'Color', [0, 0, 0])
plot(hand_high_x, 'Color', [0, 0, 0])

subplot(3, 2, 2)
for(i=1:numDemos)
    plot(hand_coord_set_x{i}, hand_coord_set_y{i}, '-o', 'Color',[i/numDemos, 0, 0])
    hold on;
end
plot(mean_hand_coord_x, mean_hand_coord_y, '-xy')

subplot(3, 2, 3)
for(i=1:numDemos)
    plot(hand_coord_set_y{i}, '-o', 'Color',[0, i/numDemos,  0])
    hold on;
end
plot(mean_hand_coord_y, '-xy')
plot(hand_high_y, 'Color', [0, 0, 0])
plot(hand_low_y, 'Color', [0, 0, 0])

subplot(3, 2, 4)
for(i=1:numDemos)
    plot(hand_coord_set_x{i}, hand_coord_set_z{i}, '-o', 'Color',[0, i/numDemos,  0])
    hold on;
end
plot(mean_hand_coord_x, mean_hand_coord_z, '-xy')

subplot(3, 2, 5)
for(i=1:numDemos)
    plot(hand_coord_set_z{i}, '-o', 'Color',[0, 0, i/numDemos])
    hold on;
end
plot(mean_hand_coord_z, '-xy')
plot(hand_low_z, 'Color', [0, 0, 0])
plot(hand_high_z, 'Color', [0, 0, 0])

subplot(3, 2, 6)
for(i=1:numDemos)
    plot(hand_coord_set_y{i}, hand_coord_set_z{i},'-o', 'Color',[0, 0, i/numDemos])
    hold on;
end
plot(mean_hand_coord_y, mean_hand_coord_z, '-xy')
hold on;

upperset={}
upperset{1} = mean_upper_coord
upperset{2} = mean_upper_coord_2
upperset{3} = mean_upper_coord_x
upperset{4} = mean_upper_coord_x_2
upperset{5} = mean_upper_coord_y
upperset{6} = mean_upper_coord_y_2
upperset{7} = mean_upper_coord_z
upperset{8} = mean_upper_coord_z_2
upperset{9} = upper_low_x
upperset{10} = upper_low_x_2
upperset{11} = upper_low_y
upperset{12} = upper_low_y_2
upperset{13} = upper_low_z
upperset{14} = upper_low_z_2
upperset{15} = upper_high_x
upperset{16} = upper_high_x_2
upperset{17} = upper_high_y
upperset{18} = upper_high_y_2
upperset{19} = upper_high_z
upperset{20} = upper_high_z_2
upperset{21} = upper_ang
upperset{22} = mean_upper_ang
upperset{23} = upper_high_ang_x
upperset{24} = upper_high_ang_y
upperset{25} = upper_high_ang_z
upperset{26} = upper_low_ang_x
upperset{27} = upper_low_ang_y
upperset{28} = upper_low_ang_z
save(upper_file, 'upperset')

lowerset={}
lowerset{1} = mean_lower_coord
lowerset{2} = mean_lower_coord_2
lowerset{3} = mean_lower_coord_x
lowerset{4} = mean_lower_coord_x_2
lowerset{5} = mean_lower_coord_y
lowerset{6} = mean_lower_coord_y_2
lowerset{7} = mean_lower_coord_z
lowerset{8} = mean_lower_coord_z_2
lowerset{9} = lower_low_x
lowerset{10} = lower_low_x_2
lowerset{11} = lower_low_y
lowerset{12} = lower_low_y_2
lowerset{13} = lower_low_z
lowerset{14} = lower_low_z_2
lowerset{15} = lower_high_x
lowerset{16} = lower_high_x_2
lowerset{17} = lower_high_y
lowerset{18} = lower_high_y_2
lowerset{19} = lower_high_z
lowerset{20} = lower_high_z_2
lowerset{21} = lower_ang
lowerset{22} = mean_lower_ang
lowerset{23} = lower_high_ang_x
lowerset{24} = lower_high_ang_y
lowerset{25} = lower_high_ang_z
lowerset{26} = lower_low_ang_x
lowerset{27} = lower_low_ang_y
lowerset{28} = lower_low_ang_z
save(lower_file, 'lowerset')

handset={}
handset{1} = mean_hand_coord
handset{2} = mean_hand_coord_2
handset{3} = mean_hand_coord_x
handset{4} = mean_hand_coord_x_2
handset{5} = mean_hand_coord_y
handset{6} = mean_hand_coord_y_2
handset{7} = mean_hand_coord_z
handset{8} = mean_hand_coord_z_2
handset{9} = hand_low_x
handset{10} = hand_low_x_2
handset{11} = hand_low_y
handset{12} = hand_low_y_2
handset{13} = hand_low_z
handset{14} = hand_low_z_2
handset{15} = hand_high_x
handset{16} = hand_high_x_2
handset{17} = hand_high_y
handset{18} = hand_high_y_2
handset{19} = hand_high_z
handset{20} = hand_high_z_2
handset{21} = hand_ang
handset{22} = mean_hand_ang
handset{23} = hand_high_ang_x
handset{24} = hand_high_ang_y
handset{25} = hand_high_ang_z
handset{26} = hand_low_ang_x
handset{27} = hand_low_ang_y
handset{28} = hand_low_ang_z
save(hand_file, 'handset')


%figure
%for(i=1:demoSize/4)
%    r = max_distance_upper(i);
%    [x, y, z] = sphere()
%    surf(x*r + mean_upper_coord(i,1), y*r+mean_upper_coord(i,2), z*r+mean_upper_coord(i,3));
%    hold on;
%    mean_upper_coord(i,:)*max_distance_upper(i)
%    sphere = surf(mean_upper_coord(i,:)*max_distance_upper(i));
%    set(sphere,'FaceColor',[0 0 1]);
%    hold on;
%    
%end

numDemos
demoSize
max_
min_
end
