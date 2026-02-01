import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import { AccidentReport, Severity } from '../types';

interface InteractiveLiveMapProps {
  accidents: AccidentReport[];
  onMarkerClick?: (accident: AccidentReport) => void;
}

export const InteractiveLiveMap: React.FC<InteractiveLiveMapProps> = ({ accidents, onMarkerClick }) => {
  const mapRef = useRef<HTMLDivElement>(null);
  const leafletMapRef = useRef<L.Map | null>(null);
  const markersRef = useRef<L.Marker[]>([]);

  useEffect(() => {
    if (!mapRef.current) return;

    // Initialize map only once
    if (!leafletMapRef.current) {
      // Coimbatore, Tamil Nadu coordinates (11.0168° N, 76.9558° E)
      leafletMapRef.current = L.map(mapRef.current).setView([11.0168, 76.9558], 13);

      // Add OpenStreetMap tile layer with dark theme
      L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
      }).addTo(leafletMapRef.current);
    }

    // Clear existing markers
    markersRef.current.forEach(marker => marker.remove());
    markersRef.current = [];

    // Add markers for accidents
    accidents.forEach(accident => {
      // Determine marker color based on severity
      const color = accident.severity === Severity.HIGH || accident.severity === Severity.CRITICAL
        ? '#ef4444'
        : accident.severity === Severity.MEDIUM
          ? '#eab308'
          : '#10b981';

      // Create custom icon
      const customIcon = L.divIcon({
        className: 'custom-marker',
        html: `
          <div style="
            width: 24px;
            height: 24px;
            background-color: ${color};
            border: 3px solid #000;
            border-radius: 50%;
            box-shadow: 0 0 10px ${color}80;
            position: relative;
          ">
            ${(accident.severity === Severity.HIGH || accident.severity === Severity.CRITICAL) ? `
              <div style="
                position: absolute;
                top: -3px;
                left: -3px;
                right: -3px;
                bottom: -3px;
                border: 2px solid ${color};
                border-radius: 50%;
                animation: pulse 2s infinite;
              "></div>
            ` : ''}
          </div>
        `,
        iconSize: [24, 24],
        iconAnchor: [12, 12],
        popupAnchor: [0, -12]
      });

      const marker = L.marker([accident.location.lat, accident.location.lng], {
        icon: customIcon
      }).addTo(leafletMapRef.current!);

      // Format timestamp
      const timeAgo = getTimeAgo(new Date(accident.timestamp));

      // Create popup content
      const popupContent = `
        <div style="color: #fff; background: #18181b; padding: 12px; border-radius: 8px; min-width: 220px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="
              background: rgba(255,255,255,0.1);
              padding: 2px 8px;
              border-radius: 4px;
              font-size: 10px;
              font-weight: bold;
              text-transform: uppercase;
            ">${accident.type}</span>
            <span style="
              font-size: 10px;
              font-weight: bold;
              color: ${color};
              text-transform: uppercase;
            ">${accident.severity}</span>
          </div>
          <p style="margin: 0 0 8px 0; font-size: 13px; line-height: 1.4;">${accident.description}</p>
          <div style="
            font-size: 11px;
            color: #a1a1aa;
            padding-top: 8px;
            border-top: 1px solid rgba(255,255,255,0.1);
            display: flex;
            justify-content: space-between;
          ">
            <span><strong style="color: #fff;">${accident.location.address}</strong></span>
          </div>
          <div style="
            font-size: 10px;
            color: #71717a;
            margin-top: 4px;
            display: flex;
            justify-content: space-between;
          ">
            <span>Status: <strong style="color: #fff;">${accident.status}</strong></span>
            <span style="color: #fbbf24;">${timeAgo}</span>
          </div>
        </div>
      `;

      marker.bindPopup(popupContent, {
        className: 'custom-popup',
        maxWidth: 300
      });

      // Add click listener
      marker.on('click', () => {
        if (onMarkerClick) {
          onMarkerClick(accident);
        }
      });

      markersRef.current.push(marker);
    });

    return () => {
      // Cleanup on unmount
      if (leafletMapRef.current) {
        markersRef.current.forEach(marker => marker.remove());
      }
    };
  }, [accidents, onMarkerClick]);

  // Helper function to calculate time ago
  const getTimeAgo = (date: Date): string => {
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;

    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours}h ago`;

    const diffDays = Math.floor(diffHours / 24);
    return `${diffDays}d ago`;
  };

  return (
    <div className="relative w-full h-full">
      <div ref={mapRef} className="w-full h-full z-0" />

      {/* Legend */}
      <div className="absolute top-4 right-4 bg-zinc-900/90 backdrop-blur-xl p-4 rounded-xl border border-white/10 shadow-2xl z-[1000]">
        <h3 className="font-bold text-white mb-3 text-sm flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
          Coimbatore Live Incidents
        </h3>
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-xs text-zinc-300">
            <span className="w-3 h-3 rounded-full bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.5)]"></span>
            High/Critical Risk
          </div>
          <div className="flex items-center gap-2 text-xs text-zinc-300">
            <span className="w-3 h-3 rounded-full bg-yellow-500 shadow-[0_0_10px_rgba(234,179,8,0.5)]"></span>
            Medium Risk
          </div>
          <div className="flex items-center gap-2 text-xs text-zinc-300">
            <span className="w-3 h-3 rounded-full bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.5)]"></span>
            Low Risk
          </div>
        </div>
        <div className="mt-3 pt-3 border-t border-white/10 text-xs text-zinc-400">
          <div className="flex items-center justify-between">
            <span>Total Incidents:</span>
            <span className="font-bold text-white">{accidents.length}</span>
          </div>
        </div>
        <div className="mt-2 text-xs text-zinc-500">
          Powered by OpenStreetMap
        </div>
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% {
            opacity: 1;
            transform: scale(1);
          }
          50% {
            opacity: 0.5;
            transform: scale(1.1);
          }
        }
        
        .custom-popup .leaflet-popup-content-wrapper {
          background: transparent;
          box-shadow: none;
          padding: 0;
        }
        
        .custom-popup .leaflet-popup-tip {
          background: #18181b;
        }
        
        .leaflet-container {
          background: #000;
        }
      `}</style>
    </div>
  );
};
