export const SUPPLIER_DATA = {
  region: 'Andhra Pradesh',
  hubName: 'Guntur Supplier Hub & Cold Chain Yard',
  kpis: {
    activeBuyerRequests: 24,
    activeBuyerRequestsChange: '+15%',
    highDemandProducts: 9,
    totalOrders: 68,
    totalOrdersChange: '+22%',
    estimatedRevenue: '₹5.8 Lakh',
    estimatedRevenueChange: '+20%'
  },
  regionalDemandPoints: [
    { city: 'Vijayawada', status: 'High Demand', color: '#EF4444', x: 45, y: 55, demand: 'High' },
    { city: 'Guntur', status: 'High Demand', color: '#EF4444', x: 40, y: 62, demand: 'High' },
    { city: 'Hyderabad', status: 'Medium Demand', color: '#F59E0B', x: 25, y: 35, demand: 'Medium' },
    { city: 'Bangalore', status: 'High Demand', color: '#EF4444', x: 30, y: 80, demand: 'High' },
    { city: 'Visakhapatnam', status: 'Low Demand', color: '#10B981', x: 75, y: 25, demand: 'Low' },
    { city: 'Kakinada', status: 'Low Demand', color: '#10B981', x: 70, y: 40, demand: 'Low' },
    { city: 'Tirupati', status: 'Medium Demand', color: '#F59E0B', x: 42, y: 85, demand: 'Medium' },
  ],
  supplierInventoryCatalog: [
    { id: 'tomato', name: 'Tomato (Fresh Hybrid)', icon: '🍅', category: 'Vegetables', wholesalePrice: 22, unit: 'kg', stockAvailable: '50,000 kg', grade: 'Grade A Export', moq: '200 kg', location: 'Guntur Cold Hub', status: 'In Stock' },
    { id: 'red_chilli', name: 'Guntur Red Chilli (Teja)', icon: '🌶️', category: 'Spices', wholesalePrice: 125, unit: 'kg', stockAvailable: '25,000 kg', grade: 'Premium Teja 1', moq: '50 kg', location: 'Guntur Yard', status: 'High Demand' },
    { id: 'basmati_rice', name: 'Basmati Rice (Royal 5kg)', icon: '🌾', category: 'Staples', wholesalePrice: 380, unit: 'bag', stockAvailable: '3,500 Bags', grade: '1121 Extra Long', moq: '20 Bags', location: 'Rajahmundry Hub', status: 'In Stock' },
    { id: 'sunflower_oil', name: 'Refined Sunflower Oil (1L)', icon: '🌻', category: 'Fats & Oils', wholesalePrice: 132, unit: 'L', stockAvailable: '8,000 Liters', grade: 'FSSAI Certified', moq: '100 Liters', location: 'Tenali Mill Yard', status: 'In Stock' },
    { id: 'potato', name: 'Potato (Indore White)', icon: '🥔', category: 'Vegetables', wholesalePrice: 28, unit: 'kg', stockAvailable: '40,000 kg', grade: 'Grade A Table', moq: '200 kg', location: 'Vijayawada Yard', status: 'In Stock' },
    { id: 'turmeric', name: 'Organic Turmeric Powder', icon: '🟡', category: 'Spices', wholesalePrice: 142, unit: 'kg', stockAvailable: '5,000 kg', grade: '99% Curcumin Pure', moq: '50 kg', location: 'Guntur Exporters', status: 'In Stock' },
    { id: 'milk', name: 'Fresh Whole Milk (500ml)', icon: '🥛', category: 'Dairy', wholesalePrice: 48, unit: 'L', stockAvailable: '12,000 L/day', grade: 'A2 Fresh Pasteurized', moq: '50 Liters', location: 'Deccan Dairy Co-op', status: 'Daily Supply' },
    { id: 'wheat_atta', name: 'Wheat Atta (Whole Grain 5kg)', icon: '🍞', category: 'Staples', wholesalePrice: 215, unit: 'bag', stockAvailable: '4,500 Bags', grade: 'MP Sharbati', moq: '15 Bags', location: 'Coastal Agro Mill', status: 'In Stock' },
    { id: 'onion', name: 'Onion (Nashik Red)', icon: '🧅', category: 'Vegetables', wholesalePrice: 32, unit: 'kg', stockAvailable: '60,000 kg', grade: 'Grade A Medium', moq: '200 kg', location: 'Mangalagiri Yard', status: 'Surplus Stock' },
    { id: 'green_chilli', name: 'Green Chilli (Hybrid)', icon: '🫑', category: 'Vegetables', wholesalePrice: 52, unit: 'kg', stockAvailable: '15,000 kg', grade: 'Spicy Long', moq: '100 kg', location: 'Kurnool Depot', status: 'High Demand' },
    { id: 'toor_dal', name: 'Toor Dal (Unpolished)', icon: '🫘', category: 'Pulses', wholesalePrice: 138, unit: 'kg', stockAvailable: '18,000 kg', grade: 'Desi Yellow', moq: '100 kg', location: 'Kakinada Hub', status: 'In Stock' },
    { id: 'paneer', name: 'Fresh Malai Paneer (200g)', icon: '🧀', category: 'Dairy', wholesalePrice: 82, unit: 'pkt', stockAvailable: '2,500 Pkts/day', grade: 'Vacuum Sealed', moq: '30 Pkts', location: 'Deccan Dairy Co-op', status: 'Daily Supply' },
  ],
  topBuyerRequests: [
    { id: 'req-1', product: 'Tomato (Fresh Hybrid)', icon: '🍅', quantity: '5,000 kg', buyer: 'Vijayawada Central Mart', location: 'Vijayawada, AP', budget: '₹1.10 Lakh', timeRemaining: '2 days left', urgent: true },
    { id: 'req-2', product: 'Onion (Nashik Red)', icon: '🧅', quantity: '3,000 kg', buyer: 'Hyderabad Supermarket Co-op', location: 'Hyderabad, TS', budget: '₹96,000', timeRemaining: '3 days left', urgent: false },
    { id: 'req-3', product: 'Guntur Red Chilli (Teja)', icon: '🌶️', quantity: '2,000 kg', buyer: 'Bangalore Spice Processing Ltd', location: 'Bangalore, KA', budget: '₹2.50 Lakh', timeRemaining: '5 days left', urgent: true },
    { id: 'req-4', product: 'Basmati Rice (Royal 5kg)', icon: '🌾', quantity: '500 Bags', buyer: 'Visakhapatnam Mega Hypermart', location: 'Visakhapatnam, AP', budget: '₹1.90 Lakh', timeRemaining: '1 day left', urgent: true },
    { id: 'req-5', product: 'Refined Sunflower Oil', icon: '🌻', quantity: '1,500 Liters', buyer: 'Tirupati Wholesale Distributors', location: 'Tirupati, AP', budget: '₹1.98 Lakh', timeRemaining: '4 days left', urgent: false },
    { id: 'req-6', product: 'Whole Wheat Atta (5kg)', icon: '🍞', quantity: '400 Bags', buyer: 'Kurnool Food Mart', location: 'Kurnool, AP', budget: '₹86,000', timeRemaining: '3 days left', urgent: false },
  ],
  activeB2BOrders: [
    { id: 'SUP-9401', retailerName: 'Guntur Retail Co-op', product: '5,000 kg Tomato', amount: 110000, date: '2026-09-14', status: 'In Transit', carrier: 'Reefer Express Truck AP-07-VT-4412' },
    { id: 'SUP-9402', retailerName: 'Vijayawada Supermart', product: '1,000 kg Red Chilli', amount: 125000, date: '2026-09-13', status: 'Dispatched', carrier: 'FastFreight Logistics 10-Ton' },
    { id: 'SUP-9403', retailerName: 'Hyderabad Express Stores', product: '200 Bags Basmati Rice', amount: 76000, date: '2026-09-12', status: 'Delivered', carrier: 'Godavari Transport Line' },
    { id: 'SUP-9404', retailerName: 'Mangalagiri Mart', product: '500 L Sunflower Oil', amount: 66000, date: '2026-09-11', status: 'Delivered', carrier: 'Tenali Local Fleet' },
  ],
  marketInsights: {
    title: 'Market Insights',
    message: 'Demand for Guntur Red Chilli is expected to increase by 26% across South India next month. Current spot rate ₹140/kg.',
    cta: 'View Demand Pie Chart →'
  },
  postSupply: {
    title: 'Post Available Supply',
    message: 'List your newly harvested crop batch and instantly reach 12,500+ connected retail buyers in AP & TS.',
    cta: 'Manage Catalog →'
  }
};

