"""
A program to read data and return statistical statistical aspects of recorded rainfall.

The aim was to learn the basics of python (no libraries were used) in regards to reading in and processing a CSV file to then produce an output of statistics from numbers within the file.

User calls main() function with a given csv file, the year of interest, and whether they want info on general statistics (type = 'stats') or on correlations (type = 'corr').

Author: David Ika
Date: 14 Sep 2020
"""
def main(csvfile, year, type):

# calcs if stats called:
    
    def calculate_stats(monthly_data): 
# form lists:
        minimum = []
        maximum = []
        average = []
        standard_deviation = []
        
        for mon in range(1,13):
            month_data = monthly_data.get(str(mon))
            if month_data:
                maximum.append(round(max(month_data),4))
                filtered_minimum = list(filter(lambda x:x, month_data))
                if filtered_minimum:
                    minimum.append(round(min(filtered_minimum),4))
                else:
                    minimum.append(0)
                mean = round(sum(month_data)/len(month_data),4)
                average.append(mean)
                
# standard deviation calc:
                standard_d = []
                for rain in month_data:
                    # Note: cannot refer to mean(), as it is rounded to 4dp
                    standard_d.append((rain-sum(month_data)/len(month_data))**2)
                standard_deviation.append(round((sum(standard_d)/len(standard_d))**0.5,4))
            else:
                maximum.append(0)
                minimum.append(0)
                average.append(0)
                standard_deviation.append(0)
        return minimum, maximum, average, standard_deviation

# calcs if corr called:
    
    def calculate_corr(first_monthly_data, second_monthly_data):
    # form lists for parts of correlation formula:
        numerator = []
        denominator1 = []
        denominator2 = []
        if first_monthly_data:
            first_mean = sum(first_monthly_data)/len(first_monthly_data)
        else:
            first_mean = 0
        if second_monthly_data:
            second_mean = sum(second_monthly_data)/len(second_monthly_data)
        else:
            second_mean = 0

        for i in range(12):
    # appending calcs to above lists:
            n = (first_monthly_data[i]-first_mean)*(second_monthly_data[i]-second_mean)
            numerator.append(n)
            d1 = (first_monthly_data[i]-first_mean)**2
            d2 = (second_monthly_data[i]-second_mean)**2
            denominator1.append(d1)
            denominator2.append(d2)
    # solving for ZeroDivisionError:
        corr = sum(numerator)/((sum(denominator1)**0.5)*(sum(denominator2)**0.5)) if ((sum(denominator1)**0.5)*(sum(denominator2)**0.5)) != 0 else 0
        return round(corr,4)

    def update_data_dict(dictionary, year, line):
        station_number, Year, Month, Day, rainfall = line.split(',')
        if rainfall.strip():
            rainfall = float(rainfall)
        else:
            rainfall = 0
        if int(year) == int(Year):
            if dictionary.get(Month):
                dictionary[Month].append(rainfall)
            else:
                dictionary[Month] = [rainfall]
    
# main argument, utilising above calcs::

    with open(csvfile,'r') as csv:
        year_x_data = {}
        year_y_data = {}
        
    # enumerating lines
        for idx, line in enumerate(csv.readlines()):
            if not idx:
                continue
            if type == 'corr':
                update_data_dict(year_x_data,year[0],line)
                update_data_dict(year_y_data,year[1],line)
            else:
                update_data_dict(year_x_data,year,line)
        year_x_minimum, year_x_maximum, year_x_average, year_x_std = calculate_stats(year_x_data)
    # final desired output:
        if type == 'stats':
            return year_x_minimum, year_x_maximum, year_x_average, year_x_std
        elif type == 'corr':
            year_y_minimum, year_y_maximum, year_y_average, year_y_std = calculate_stats(year_y_data)
            return (calculate_corr(year_x_minimum, year_y_minimum),
                    calculate_corr(year_x_maximum, year_y_maximum),
                    calculate_corr(year_x_average, year_y_average),
                    calculate_corr(year_x_std, year_y_std))
# fin