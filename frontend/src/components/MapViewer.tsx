import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet'
import L from 'leaflet'

interface Props {
  center?: [number, number]
}

const markerIcon = new L.Icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
})

export default function MapViewer({ center = [28.6139, 77.209] }: Props) {
  return (
    <div className="overflow-hidden rounded-3xl border border-white/10 bg-slate-950/70 p-3 shadow-2xl shadow-slate-950/25 backdrop-blur-xl">
      <div className="px-2 pb-3 pt-2">
        <p className="text-xs uppercase tracking-[0.35em] text-cyan-200/60">GIS Map</p>
        <h3 className="mt-2 text-xl font-semibold text-white">Scene location and spatial context</h3>
      </div>
      <div className="h-72 overflow-hidden rounded-2xl border border-white/10">
        <MapContainer center={center} zoom={6} scrollWheelZoom className="h-full w-full">
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <Marker position={center} icon={markerIcon}>
            <Popup>Analyzed satellite footprint</Popup>
          </Marker>
        </MapContainer>
      </div>
    </div>
  )
}
