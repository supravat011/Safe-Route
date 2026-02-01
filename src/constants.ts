import { AccidentType, Severity, AccidentReport, Hospital, SafetyTip } from './types';

// Coimbatore coordinates: 11.0168° N, 76.9558° E
export const COIMBATORE_CENTER = { lat: 11.0168, lng: 76.9558 };

// Real accident-prone zones in Coimbatore
export const MOCK_REPORTS: AccidentReport[] = [
  // HIGH RISK ZONES
  {
    id: '1',
    type: AccidentType.COLLISION,
    severity: Severity.HIGH,
    description: 'Multi-vehicle collision at busy junction during peak hours.',
    location: { lat: 11.0168, lng: 76.9558, address: 'Gandhipuram Central' },
    timestamp: new Date(Date.now() - 30 * 60000).toISOString(), // 30 mins ago
    status: 'Verified'
  },
  {
    id: '2',
    type: AccidentType.PEDESTRIAN,
    severity: Severity.CRITICAL,
    description: 'Pedestrian hit at crosswalk near shopping complex.',
    location: { lat: 11.0048, lng: 76.9618, address: 'RS Puram Junction' },
    timestamp: new Date(Date.now() - 45 * 60000).toISOString(), // 45 mins ago
    status: 'Pending'
  },
  {
    id: '3',
    type: AccidentType.COLLISION,
    severity: Severity.HIGH,
    description: 'Two-wheeler collision with car at signal.',
    location: { lat: 10.9925, lng: 76.9619, address: 'Avinashi Road' },
    timestamp: new Date(Date.now() - 60 * 60000).toISOString(), // 1 hour ago
    status: 'Verified'
  },
  {
    id: '4',
    type: AccidentType.ROLLOVER,
    severity: Severity.CRITICAL,
    description: 'Vehicle rollover on highway due to overspeeding.',
    location: { lat: 11.0510, lng: 77.0229, address: 'Sathy Road' },
    timestamp: new Date(Date.now() - 90 * 60000).toISOString(), // 1.5 hours ago
    status: 'Verified'
  },

  // MEDIUM RISK ZONES
  {
    id: '5',
    type: AccidentType.BREAKDOWN,
    severity: Severity.MEDIUM,
    description: 'Vehicle breakdown blocking left lane.',
    location: { lat: 11.0271, lng: 76.9635, address: 'Trichy Road' },
    timestamp: new Date(Date.now() - 20 * 60000).toISOString(), // 20 mins ago
    status: 'Resolved'
  },
  {
    id: '6',
    type: AccidentType.COLLISION,
    severity: Severity.MEDIUM,
    description: 'Minor collision at roundabout.',
    location: { lat: 10.9854, lng: 76.9558, address: 'Peelamedu' },
    timestamp: new Date(Date.now() - 120 * 60000).toISOString(), // 2 hours ago
    status: 'Verified'
  },
  {
    id: '7',
    type: AccidentType.OBSTRUCTION,
    severity: Severity.MEDIUM,
    description: 'Fallen tree branch partially blocking road.',
    location: { lat: 11.0412, lng: 76.9734, address: 'Mettupalayam Road' },
    timestamp: new Date(Date.now() - 150 * 60000).toISOString(), // 2.5 hours ago
    status: 'Verified'
  },

  // LOW RISK ZONES
  {
    id: '8',
    type: AccidentType.BREAKDOWN,
    severity: Severity.LOW,
    description: 'Parked vehicle with hazard lights on shoulder.',
    location: { lat: 11.0089, lng: 76.9339, address: 'Saibaba Colony' },
    timestamp: new Date(Date.now() - 180 * 60000).toISOString(), // 3 hours ago
    status: 'Resolved'
  },
  {
    id: '9',
    type: AccidentType.OTHER,
    severity: Severity.LOW,
    description: 'Minor fender bender, no injuries.',
    location: { lat: 10.9965, lng: 76.9708, address: 'Hopes College' },
    timestamp: new Date(Date.now() - 200 * 60000).toISOString(), // 3.3 hours ago
    status: 'Resolved'
  },
  {
    id: '10',
    type: AccidentType.PEDESTRIAN,
    severity: Severity.MEDIUM,
    description: 'Near-miss incident at pedestrian crossing.',
    location: { lat: 11.0321, lng: 76.9912, address: 'Singanallur' },
    timestamp: new Date(Date.now() - 240 * 60000).toISOString(), // 4 hours ago
    status: 'Verified'
  },
  {
    id: '11',
    type: AccidentType.COLLISION,
    severity: Severity.HIGH,
    description: 'Head-on collision between bus and truck.',
    location: { lat: 10.9634, lng: 76.9012, address: 'Pollachi Road' },
    timestamp: new Date(Date.now() - 15 * 60000).toISOString(), // 15 mins ago
    status: 'Pending'
  },
  {
    id: '12',
    type: AccidentType.BREAKDOWN,
    severity: Severity.LOW,
    description: 'Auto rickshaw breakdown on service road.',
    location: { lat: 11.0145, lng: 77.0024, address: 'Kalapatti' },
    timestamp: new Date(Date.now() - 300 * 60000).toISOString(), // 5 hours ago
    status: 'Resolved'
  }
];

export const MOCK_HOSPITALS: Hospital[] = [
  {
    id: 'h1',
    name: 'Coimbatore Medical College Hospital',
    distance: '1.2 km',
    contact: '0422-2530222',
    lat: 11.0049,
    lng: 76.9645,
    type: 'Hospital'
  },
  {
    id: 'h2',
    name: 'PSG Hospitals',
    distance: '2.5 km',
    contact: '0422-2570170',
    lat: 10.9965,
    lng: 76.9708,
    type: 'Hospital'
  },
  {
    id: 'h3',
    name: 'Kovai Medical Center',
    distance: '3.1 km',
    contact: '0422-4324000',
    lat: 11.0271,
    lng: 76.9635,
    type: 'Hospital'
  },
  {
    id: 'p1',
    name: 'Gandhipuram Police Station',
    distance: '0.8 km',
    contact: '0422-2394100',
    lat: 11.0183,
    lng: 76.9674,
    type: 'Police'
  },
  {
    id: 'p2',
    name: 'RS Puram Police Station',
    distance: '1.5 km',
    contact: '0422-2544100',
    lat: 11.0048,
    lng: 76.9518,
    type: 'Police'
  },
  {
    id: 'f1',
    name: 'Coimbatore Fire Station',
    distance: '1.0 km',
    contact: '0422-2394444',
    lat: 11.0125,
    lng: 76.9589,
    type: 'Fire'
  }
];

export const STATIC_SAFETY_TIPS: SafetyTip[] = [
  {
    title: 'Wear Your Helmet',
    content: 'Always wear a certified helmet while riding a two-wheeler. It reduces the risk of severe head injury by 70%.',
    category: 'Rule',
    icon: 'helmet'
  },
  {
    title: 'Don\'t Drink and Drive',
    content: 'Alcohol impairs reaction time and judgment. Use a designated driver or taxi service.',
    category: 'Warning',
    icon: 'beer-off'
  },
  {
    title: 'Respect Speed Limits',
    content: 'Speed limits are set for optimal safety. Higher speeds increase stopping distance and severity of impact.',
    category: 'Tip',
    icon: 'gauge'
  }
];