// lib/screens/dashboard_screen.dart
import 'package:flutter/material.dart';
import 'package:table_calendar/table_calendar.dart';
import 'package:fl_chart/fl_chart.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  DateTime _focusedDay = DateTime.now();
  DateTime _selectedDay = DateTime.utc(2025, 6, 21);

  final Map<String, Map<String, int>> activityData = {
    '2025-06-21': {'calories': 612, 'carbs': 90, 'fat': 25},
    '2025-06-22': {'calories': 730, 'carbs': 105, 'fat': 30},
    '2025-06-23': {'calories': 450, 'carbs': 60, 'fat': 20},
    '2025-06-25': {'calories': 500, 'carbs': 70, 'fat': 22},
    '2025-06-26': {'calories': 300, 'carbs': 40, 'fat': 10},
  };

  Map<String, int> calculateMonthlyTotals(String monthPrefix) {
    int totalCalories = 0;
    int totalCarbs = 0;
    int totalFat = 0;

    activityData.forEach((date, values) {
      if (date.startsWith(monthPrefix)) {
        totalCalories += values['calories'] ?? 0;
        totalCarbs += values['carbs'] ?? 0;
        totalFat += values['fat'] ?? 0;
      }
    });

    return {
      'calories': totalCalories,
      'carbs': totalCarbs,
      'fat': totalFat,
    };
  }

  @override
  Widget build(BuildContext context) {
    final String dateKey = _selectedDay.toIso8601String().substring(0, 10);
    final String monthKey = _focusedDay.toIso8601String().substring(0, 7);
    final selectedData = activityData[dateKey];
    final monthTotals = calculateMonthlyTotals(monthKey);

    return Scaffold(
      appBar: AppBar(
        title: Text('📆 Strava Dashboard'),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            TableCalendar(
              firstDay: DateTime.utc(2025, 6, 1),
              lastDay: DateTime.utc(2025, 12, 31),
              focusedDay: _focusedDay,
              selectedDayPredicate: (day) => isSameDay(_selectedDay, day),
              onDaySelected: (selectedDay, focusedDay) {
                setState(() {
                  _selectedDay = selectedDay;
                  _focusedDay = focusedDay;
                });
              },
              calendarStyle: CalendarStyle(
                todayDecoration: BoxDecoration(
                  color: Colors.deepOrange.shade200,
                  shape: BoxShape.circle,
                ),
                selectedDecoration: BoxDecoration(
                  color: Colors.deepOrange,
                  shape: BoxShape.circle,
                ),
              ),
            ),
            if (selectedData != null) ...[
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Card(
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12)),
                  elevation: 4,
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('📅 $dateKey',
                            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                        SizedBox(height: 10),
                        Text('🔥 Calorieën: ${selectedData['calories']} kcal'),
                        Text('🍞 Koolhydraten: ${selectedData['carbs']} g'),
                        Text('🥑 Vet: ${selectedData['fat']} g'),
                      ],
                    ),
                  ),
                ),
              )
            ] else ...[
              Padding(
                padding: const EdgeInsets.all(24.0),
                child: Text('Geen data voor deze datum.', style: TextStyle(color: Colors.grey)),
              )
            ],
            SizedBox(
              height: 220,
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16.0),
                child: BarChart(
                  BarChartData(
                    barGroups: [
                      BarChartGroupData(x: 0, barRods: [
                        BarChartRodData(toY: monthTotals['calories']!.toDouble(), color: Colors.redAccent)
                      ]),
                      BarChartGroupData(x: 1, barRods: [
                        BarChartRodData(toY: monthTotals['carbs']!.toDouble(), color: Colors.orange)
                      ]),
                      BarChartGroupData(x: 2, barRods: [
                        BarChartRodData(toY: monthTotals['fat']!.toDouble(), color: Colors.green)
                      ]),
                    ],
                    titlesData: FlTitlesData(
                      bottomTitles: AxisTitles(
                        sideTitles: SideTitles(showTitles: true, getTitlesWidget: (value, _) {
                          switch (value.toInt()) {
                            case 0:
                              return Text('Kcal');
                            case 1:
                              return Text('KH');
                            case 2:
                              return Text('Vet');
                            default:
                              return Text('');
                          }
                        }),
                      ),
                      leftTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                      topTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                      rightTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                    ),
                    borderData: FlBorderData(show: false),
                  ),
                ),
              ),
            )
          ],
        ),
      ),
    );
  }
}
