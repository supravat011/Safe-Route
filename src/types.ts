export enum Severity {
  LOW = 'Low',
  MEDIUM = 'Medium',
  HIGH = 'High',
  CRITICAL = 'Critical'
}

export enum AccidentType {
  COLLISION = 'Vehicle Collision',
  PEDESTRIAN = 'Pedestrian Incident',
  ROLLOVER = 'Rollover',
  BREAKDOWN = 'Vehicle Breakdown',
  OBSTRUCTION = 'Road Obstruction',
  OTHER = 'Other'
}

export enum PageView {
  HOME = 'home',
  REPORT = 'report',
  MAP = 'map',
  SAFETY = 'safety',
  EMERGENCY = 'emergency',
  ADMIN = 'admin'
}

export interface AccidentReport {
  id: string;
  type: AccidentType;
  severity: Severity;
  description: string;
  location: { lat: number; lng: number; address?: string };
  timestamp: string;
  status: 'Pending' | 'Verified' | 'Resolved';
  imageUrl?: string;
}

export interface Hospital {
  id: string;
  name: string;
  distance: string;
  contact: string;
  lat: number;
  lng: number;
  type: 'Hospital' | 'Police' | 'Fire';
}

export interface SafetyTip {
  title: string;
  content: string;
  category: 'Rule' | 'Tip' | 'Warning';
  icon: string;
}