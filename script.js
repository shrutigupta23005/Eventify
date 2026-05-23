fetch('locations.json')
  .then(res => res.json())
  .then(data => {
    data.forEach(loc => {
      L.marker([loc.lat, loc.lng]).addTo(map)
        .bindPopup(`<b>${loc.name}</b>`);
    });
  });

  