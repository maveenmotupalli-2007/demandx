export const RETAILER_DATA = {
  storeName: 'My Store - Guntur, AP',
  kpis: {
    predictedDemand: '1,250 units',
    predictedDemandChange: '+18%',
    currentStock: '800 units',
    currentStockChange: '-10%',
    recommendedStock: '1,300 units',
    potentialRevenue: '₹1.8 Lakh',
    potentialRevenueChange: '+22%'
  },
  demandForecastTomato: [
    { week: 'W1', actual: 800, predicted: 750 },
    { week: 'W2', actual: 1100, predicted: 1200 },
    { week: 'W3', actual: 1400, predicted: 1500 },
    { week: 'W4', actual: 1700, predicted: 1900 },
    { week: 'W5', actual: 2000, predicted: 2300 },
    { week: 'W6', actual: 2100, predicted: 2700 },
  ],
  topSellingProducts: [
    { name: 'Tomato', icon: '🍅', sales: '320 units', growth: '+25%' },
    { name: 'Onion', icon: '🧅', sales: '280 units', growth: '+18%' },
    { name: 'Red Chilli', icon: '🌶️', sales: '150 units', growth: '+12%' },
    { name: 'Potato', icon: '🥔', sales: '120 units', growth: '+8%' },
    { name: 'Cooking Oil', icon: '🛢️', sales: '110 units', growth: '+20%' },
  ],
  aiInsight: {
    title: 'AI Insight',
    message: 'Tomato demand will increase by 22% next month in your area. Consider increasing stock.',
    cta: 'View Forecast →'
  },
  supplierOffers: {
    title: 'Supplier Offers',
    message: 'Get best prices from verified suppliers.',
    cta: 'View Suppliers →'
  }
};

export const getDynamicRetailerData = (storeLocation: string) => {
  let mult = 1.0;
  let locTag = 'Guntur APMC Zone';
  if (storeLocation.includes('Vijayawada')) {
    mult = 1.45;
    locTag = 'Vijayawada Metro Hub';
  } else if (storeLocation.includes('Hyderabad')) {
    mult = 2.1;
    locTag = 'Hyderabad Urban Sector';
  }

  const demandForecastTomato = [
    { week: 'W1', actual: Math.round(800 * mult), predicted: Math.round(750 * mult) },
    { week: 'W2', actual: Math.round(1100 * mult), predicted: Math.round(1200 * mult) },
    { week: 'W3', actual: Math.round(1400 * mult), predicted: Math.round(1500 * mult) },
    { week: 'W4', actual: Math.round(1700 * mult), predicted: Math.round(1900 * mult) },
    { week: 'W5', actual: Math.round(2000 * mult), predicted: Math.round(2300 * mult) },
    { week: 'W6', actual: Math.round(2100 * mult), predicted: Math.round(2700 * mult) },
  ];

  const categoryPieData = storeLocation.includes('Hyderabad') ? [
    { name: 'Red Chilli & Spices', value: Math.round(840 * mult), color: '#EF4444' },
    { name: 'Tomato', value: Math.round(720 * mult), color: '#10B981' },
    { name: 'Onion', value: Math.round(520 * mult), color: '#8B5CF6' },
    { name: 'Cooking Oil', value: Math.round(310 * mult), color: '#F97316' },
    { name: 'Potato', value: Math.round(210 * mult), color: '#3B82F6' },
  ] : storeLocation.includes('Vijayawada') ? [
    { name: 'Tomato', value: Math.round(950 * mult), color: '#10B981' },
    { name: 'Onion', value: Math.round(620 * mult), color: '#8B5CF6' },
    { name: 'Cooking Oil', value: Math.round(410 * mult), color: '#F97316' },
    { name: 'Red Chilli', value: Math.round(360 * mult), color: '#EF4444' },
    { name: 'Potato', value: Math.round(210 * mult), color: '#3B82F6' },
  ] : [
    { name: 'Tomato', value: Math.round(320), color: '#10B981' },
    { name: 'Onion', value: Math.round(280), color: '#8B5CF6' },
    { name: 'Red Chilli', value: Math.round(150), color: '#EF4444' },
    { name: 'Potato', value: Math.round(120), color: '#3B82F6' },
    { name: 'Cooking Oil', value: Math.round(110), color: '#F97316' },
  ];

  const topSellingProducts = [
    { name: 'Tomato', icon: '🍅', sales: `${Math.round(320 * mult)} units`, growth: '+25%' },
    { name: 'Onion', icon: '🧅', sales: `${Math.round(280 * mult)} units`, growth: '+18%' },
    { name: 'Red Chilli', icon: '🌶️', sales: `${Math.round(150 * mult)} units`, growth: '+12%' },
    { name: 'Potato', icon: '🥔', sales: `${Math.round(120 * mult)} units`, growth: '+8%' },
    { name: 'Cooking Oil', icon: '🛢️', sales: `${Math.round(110 * mult)} units`, growth: '+20%' },
  ];

  const priceTrendsData = [
    { item: 'Tomato', spot: Math.round(24 * (storeLocation.includes('Hyderabad') ? 1.2 : storeLocation.includes('Vijayawada') ? 1.1 : 1.0)), wholesale: Math.round(22 * (storeLocation.includes('Hyderabad') ? 1.2 : storeLocation.includes('Vijayawada') ? 1.1 : 1.0)) },
    { item: 'Red Chilli', spot: Math.round(140 * (storeLocation.includes('Hyderabad') ? 1.15 : storeLocation.includes('Vijayawada') ? 1.08 : 1.0)), wholesale: Math.round(125 * (storeLocation.includes('Hyderabad') ? 1.15 : storeLocation.includes('Vijayawada') ? 1.08 : 1.0)) },
    { item: 'Basmati Rice', spot: Math.round(420 * (storeLocation.includes('Hyderabad') ? 1.1 : storeLocation.includes('Vijayawada') ? 1.05 : 1.0)), wholesale: Math.round(380 * (storeLocation.includes('Hyderabad') ? 1.1 : storeLocation.includes('Vijayawada') ? 1.05 : 1.0)) },
    { item: 'Sunflower Oil', spot: Math.round(145 * (storeLocation.includes('Hyderabad') ? 1.12 : storeLocation.includes('Vijayawada') ? 1.06 : 1.0)), wholesale: Math.round(132 * (storeLocation.includes('Hyderabad') ? 1.12 : storeLocation.includes('Vijayawada') ? 1.06 : 1.0)) },
    { item: 'Potato', spot: Math.round(32 * (storeLocation.includes('Hyderabad') ? 1.25 : storeLocation.includes('Vijayawada') ? 1.1 : 1.0)), wholesale: Math.round(28 * (storeLocation.includes('Hyderabad') ? 1.25 : storeLocation.includes('Vijayawada') ? 1.1 : 1.0)) },
    { item: 'Turmeric', spot: Math.round(160 * (storeLocation.includes('Hyderabad') ? 1.18 : storeLocation.includes('Vijayawada') ? 1.07 : 1.0)), wholesale: Math.round(142 * (storeLocation.includes('Hyderabad') ? 1.18 : storeLocation.includes('Vijayawada') ? 1.07 : 1.0)) },
    { item: 'Wheat Atta', spot: Math.round(240 * (storeLocation.includes('Hyderabad') ? 1.1 : storeLocation.includes('Vijayawada') ? 1.04 : 1.0)), wholesale: Math.round(215 * (storeLocation.includes('Hyderabad') ? 1.1 : storeLocation.includes('Vijayawada') ? 1.04 : 1.0)) },
    { item: 'Onion', spot: Math.round(38 * (storeLocation.includes('Hyderabad') ? 1.22 : storeLocation.includes('Vijayawada') ? 1.12 : 1.0)), wholesale: Math.round(32 * (storeLocation.includes('Hyderabad') ? 1.22 : storeLocation.includes('Vijayawada') ? 1.12 : 1.0)) },
  ];

  const annualSalesData = [
    { month: 'Jan', revenue: Math.round(140000 * mult), profit: Math.round(33600 * mult) },
    { month: 'Feb', revenue: Math.round(152000 * mult), profit: Math.round(36480 * mult) },
    { month: 'Mar', revenue: Math.round(165000 * mult), profit: Math.round(39600 * mult) },
    { month: 'Apr', revenue: Math.round(172000 * mult), profit: Math.round(41280 * mult) },
    { month: 'May', revenue: Math.round(185000 * mult), profit: Math.round(44400 * mult) },
    { month: 'Jun', revenue: Math.round(198000 * mult), profit: Math.round(47520 * mult) },
    { month: 'Jul', revenue: Math.round(210000 * mult), profit: Math.round(50400 * mult) },
    { month: 'Aug', revenue: Math.round(225000 * mult), profit: Math.round(54000 * mult) },
    { month: 'Sep (Now)', revenue: Math.round(245000 * mult), profit: Math.round(58800 * mult) },
    { month: 'Oct (FC)', revenue: Math.round(268000 * mult), profit: Math.round(64320 * mult) },
    { month: 'Nov (FC)', revenue: Math.round(285000 * mult), profit: Math.round(68400 * mult) },
    { month: 'Dec (FC)', revenue: Math.round(310000 * mult), profit: Math.round(74400 * mult) },
  ];

  const kpis = {
    predictedDemand: `${Math.round(1250 * mult).toLocaleString()} units`,
    predictedDemandChange: storeLocation.includes('Hyderabad') ? '+31%' : storeLocation.includes('Vijayawada') ? '+24%' : '+18%',
    currentStock: `${Math.round(800 * mult).toLocaleString()} units`,
    currentStockChange: storeLocation.includes('Hyderabad') ? '+12%' : storeLocation.includes('Vijayawada') ? '-5%' : '-10%',
    recommendedStock: `${Math.round(1300 * mult).toLocaleString()} units`,
    potentialRevenue: `₹${(1.8 * mult).toFixed(1)} Lakh`,
    potentialRevenueChange: storeLocation.includes('Hyderabad') ? '+35%' : storeLocation.includes('Vijayawada') ? '+29%' : '+22%'
  };

  return { demandForecastTomato, categoryPieData, topSellingProducts, priceTrendsData, annualSalesData, kpis, locTag };
};

