document.addEventListener('DOMContentLoaded', () => {
    const mapa = L.map('mapa').setView([4.7, -74.1], 8);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(mapa);

    const aparcaderosMap = {};

    aparcaderos_data.forEach(ap => {
        const marcador = L.marker([ap.lat, ap.lon])
            .addTo(mapa)
            .bindPopup(`<b>${ap.nombre}</b><br>Capacidad: ${ap.capacidad}<br>Ocupación: ${ap.ocupacion}`);
        aparcaderosMap[ap.nombre] = { ...ap, marcador };
    });

    if (typeof ultimo_bus_id !== 'undefined' && ultimo_bus_id !== null) {
        const bus = buses_data.find(b => b.id === ultimo_bus_id);
        if (bus) {
            fetch(`/api/recorrido/${bus.id}`)
                .then(res => res.json())
                .then(data => {
                    if (data.error) return;
                    const { lat1, lon1, lat2, lon2, tiempo } = data;

                    const pasos = 20;
                    const delay = 2000 / pasos;

                    const deltaLat = (lat2 - lat1) / pasos;
                    const deltaLon = (lon2 - lon1) / pasos;

                    const marcador = L.marker([lat1, lon1], {
                        icon: L.divIcon({
                            className: 'emoji-marker',
                            html: '<div style="font-size: 44px;">🚌</div>',
                            iconSize: [44, 44],
                            iconAnchor: [22, 22]
                        })
                    }).addTo(mapa);

                    let paso = 0;
                    const mover = () => {
                        if (paso <= pasos) {
                            marcador.setLatLng([lat1 + deltaLat * paso, lon1 + deltaLon * paso]);
                            paso++;
                            setTimeout(mover, delay);
                        } else {
                            // hora_salida del usuario (hh:mm)
                            const [hh, mm] = bus.hora_salida.split(':').map(n => parseInt(n));
                            const salida = new Date();
                            salida.setHours(hh, mm, 0);

                            const llegada = new Date(salida.getTime() + tiempo * 60000);
                            const horaLlegada = llegada.toTimeString().split(':').slice(0, 2).join(':');
                            const minutos = Math.round(tiempo);

                            marcador.bindPopup(`🚌 Llegada: ${horaLlegada}<br>Duración: ${minutos} minutos`).openPopup();
                        }
                    };
                    mover();
                });
        }
    }
});