const createGauge = (dato , id) => (
    new JustGage({
        id: id, // the id of the html element
        value: dato,
        symbol: "°C",
        min: 0,
        max: 100,
        decimals: 0,
        gaugeWidthScale: 0.6
    })
)