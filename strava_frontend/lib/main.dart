// lib/main.dart
import 'package:flutter/material.dart';
import 'screens/dashboard_screen.dart';

void main() {
  runApp(const StravaApp());
}

class StravaApp extends StatelessWidget {
  const StravaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Strava App',
      theme: ThemeData(
        primarySwatch: Colors.deepOrange,
        useMaterial3: true,
      ),
      home: const MainNavigation(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class MainNavigation extends StatefulWidget {
  const MainNavigation({super.key});

  @override
  State<MainNavigation> createState() => _MainNavigationState();
}

class _MainNavigationState extends State<MainNavigation> {
  int _selectedIndex = 0;

  static final List<Widget> _screens = <Widget>[
    Center(child: Text('🏠 Welkom bij je Strava Herstel App!', style: TextStyle(fontSize: 18))),
    DashboardScreen(),
    Center(child: Text('👤 Gebruikersinstellingen', style: TextStyle(fontSize: 18))),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(child: _screens[_selectedIndex]),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
        selectedItemColor: Colors.deepOrange,
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.calendar_today), label: 'Calendar'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'User'),
        ],
      ),
    );
  }
}
