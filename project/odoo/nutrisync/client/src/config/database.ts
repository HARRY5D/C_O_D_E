import * as SQLite from 'expo-sqlite';

const db = SQLite.openDatabase('nutrisync.db');

export const createTables = () => {
  db.transaction(tx => {
    tx.executeSql(
      `CREATE TABLE IF NOT EXISTS health_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        value REAL,
        unit TEXT,
        trend TEXT
      );`
    );

    tx.executeSql(
      `CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_name TEXT,
        specialty TEXT,
        phone TEXT,
        email TEXT,
        date TEXT,
        time TEXT
      );`
    );

    tx.executeSql(
      `CREATE TABLE IF NOT EXISTS meditation_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        duration INTEGER,
        category TEXT
      );`
    );

    tx.executeSql(
      `CREATE TABLE IF NOT EXISTS fitness_activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        duration INTEGER,
        calories INTEGER,
        date TEXT
      );`
    );

    tx.executeSql(
      `CREATE TABLE IF NOT EXISTS mental_health_resources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        type TEXT,
        description TEXT,
        url TEXT
      );`
    );
  });
};

export const insertHealthMetric = (name, value, unit, trend) => {
  db.transaction(tx => {
    tx.executeSql(
      'INSERT INTO health_metrics (name, value, unit, trend) VALUES (?, ?, ?, ?);',
      [name, value, unit, trend]
    );
  });
};

export const insertAppointment = (doctor_name, specialty, phone, email, date, time) => {
  db.transaction(tx => {
    tx.executeSql(
      'INSERT INTO appointments (doctor_name, specialty, phone, email, date, time) VALUES (?, ?, ?, ?, ?, ?);',
      [doctor_name, specialty, phone, email, date, time]
    );
  });
};

export const insertMeditationSession = (title, duration, category) => {
  db.transaction(tx => {
    tx.executeSql(
      'INSERT INTO meditation_sessions (title, duration, category) VALUES (?, ?, ?);',
      [title, duration, category]
    );
  });
};

export const insertFitnessActivity = (name, duration, calories, date) => {
  db.transaction(tx => {
    tx.executeSql(
      'INSERT INTO fitness_activities (name, duration, calories, date) VALUES (?, ?, ?, ?);',
      [name, duration, calories, date]
    );
  });
};

export const insertMentalHealthResource = (title, type, description, url) => {
  db.transaction(tx => {
    tx.executeSql(
      'INSERT INTO mental_health_resources (title, type, description, url) VALUES (?, ?, ?, ?);',
      [title, type, description, url]
    );
  });
};
