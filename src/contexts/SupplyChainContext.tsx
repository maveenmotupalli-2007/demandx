import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import type {
  CustomerOrder,
  RetailerProcurementOrder,
  RetailerProcurementItem,
} from '../types/firestore';
import {
  addCustomerOrderDoc,
  subscribeCustomerOrders,
  addProcurementOrderDoc,
  subscribeProcurementOrders,
  updateProcurementOrderStatusDoc,
  subscribeInventory,
} from '../services/firestoreService';
import { useAuth } from './AuthContext';

interface SupplyChainContextType {
  customerOrders: CustomerOrder[];
  procurementOrders: RetailerProcurementOrder[];
  inventoryOverrides: Record<string, number>;

  // Required API functions
  addCustomerOrder: (orderData: Omit<CustomerOrder, 'id'>) => Promise<string>;
  createRetailerStockOrder: (
    items: RetailerProcurementItem[],
    supplierId?: string,
    supplierName?: string,
    retailerId?: string,
    retailerName?: string
  ) => Promise<string>;
  fulfillSupplierOrder: (orderId: string) => Promise<void>;
  updateInventory: (productId: string, deltaQuantity: number) => void;
  getRetailerInventory: (productId: string, baseStock: number) => number;
  getCustomerOrders: (retailerId?: string) => CustomerOrder[];
  getRetailerProcurementOrders: (retailerId?: string) => RetailerProcurementOrder[];
  getSupplierBuyerRequests: (supplierId?: string) => RetailerProcurementOrder[];
}

const INITIAL_CUSTOMER_ORDERS: CustomerOrder[] = [
  {
    id: 'DX-10420',
    customerId: 'cust_01',
    customerName: 'Durga Prasad',
    retailerId: 'GUNTUR_STORE_01',
    items: [
      { productId: 'tomato', productName: 'Fresh Farm Tomato', quantity: 10, unit: 'kg', price: 24 },
      { productId: 'onion', productName: 'Nashik Quality Red Onion', quantity: 5, unit: 'kg', price: 24 },
    ],
    totalAmount: 360,
    status: 'Completed',
    paymentMethod: 'VyaPulse',
    createdAt: '10 Sep 2026',
  },
  {
    id: 'DX-10418',
    customerId: 'cust_02',
    customerName: 'Srinivas Rao',
    retailerId: 'GUNTUR_STORE_01',
    items: [
      { productId: 'basmati-rice', productName: 'India Gate Royal Basmati Rice', quantity: 2, unit: '5kg bag', price: 510 },
      { productId: 'cooking-oil', productName: 'Fortune Sunlite Sunflower Oil', quantity: 3, unit: 'Liter pouch', price: 135 },
    ],
    totalAmount: 1425,
    status: 'Completed',
    paymentMethod: 'UPI',
    createdAt: '08 Sep 2026',
  },
];

const INITIAL_PROCUREMENT_ORDERS: RetailerProcurementOrder[] = [
  {
    id: 'PO-9402',
    retailerId: 'GUNTUR_STORE_01',
    retailerName: 'My Store - Guntur, AP',
    supplierId: 'GUNTUR_SUPPLIER_HUB',
    supplierName: 'Guntur Spice Traders & Exporters',
    items: [
      { productId: 'tomato', productName: 'Fresh Farm Tomato', quantity: 5000, unit: 'kg', price: 22 },
      { productId: 'red-chilli', productName: 'Guntur Supreme Red Chilli', quantity: 2000, unit: 'kg', price: 110 },
    ],
    totalAmount: 330000,
    status: 'Dispatched',
    createdAt: '09 Sep 2026',
    dispatchedAt: '10 Sep 2026',
  },
];

const SupplyChainContext = createContext<SupplyChainContextType | undefined>(undefined);

export const SupplyChainProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { currentUser } = useAuth();

  const [customerOrders, setCustomerOrders] = useState<CustomerOrder[]>(() => {
    try {
      const saved = localStorage.getItem('demandx_sc_customer_orders');
      return saved ? JSON.parse(saved) : INITIAL_CUSTOMER_ORDERS;
    } catch {
      return INITIAL_CUSTOMER_ORDERS;
    }
  });

  const [procurementOrders, setProcurementOrders] = useState<RetailerProcurementOrder[]>(() => {
    try {
      const saved = localStorage.getItem('demandx_sc_procurement_orders');
      return saved ? JSON.parse(saved) : INITIAL_PROCUREMENT_ORDERS;
    } catch {
      return INITIAL_PROCUREMENT_ORDERS;
    }
  });

  const [inventoryOverrides, setInventoryOverrides] = useState<Record<string, number>>(() => {
    try {
      const saved = localStorage.getItem('demandx_inventory_overrides');
      return saved ? JSON.parse(saved) : {};
    } catch {
      return {};
    }
  });

  // Subscribe to real-time Firestore customerOrders with unmount cleanup
  useEffect(() => {
    let isSubscribed = true;
    const unsubscribe = subscribeCustomerOrders((orders) => {
      if (isSubscribed && orders && orders.length > 0) {
        setCustomerOrders(orders);
      }
    });
    return () => {
      isSubscribed = false;
      if (typeof unsubscribe === 'function') unsubscribe();
    };
  }, []);

  // Subscribe to real-time Firestore procurementOrders with unmount cleanup
  useEffect(() => {
    let isSubscribed = true;
    const unsubscribe = subscribeProcurementOrders((orders) => {
      if (isSubscribed && orders && orders.length > 0) {
        setProcurementOrders(orders);
      }
    });
    return () => {
      isSubscribed = false;
      if (typeof unsubscribe === 'function') unsubscribe();
    };
  }, []);

  // Subscribe to real-time Firestore inventory stock changes
  useEffect(() => {
    let isSubscribed = true;
    const unsubscribe = subscribeInventory((invMap) => {
      if (isSubscribed && invMap) {
        setInventoryOverrides((prev) => ({
          ...prev,
          ...invMap,
        }));
      }
    });
    return () => {
      isSubscribed = false;
      if (typeof unsubscribe === 'function') unsubscribe();
    };
  }, []);

  useEffect(() => {
    try {
      localStorage.setItem('demandx_sc_customer_orders', JSON.stringify(customerOrders));
    } catch (e) {
      console.warn('LocalStorage error:', e);
    }
  }, [customerOrders]);

  useEffect(() => {
    try {
      localStorage.setItem('demandx_sc_procurement_orders', JSON.stringify(procurementOrders));
    } catch (e) {
      console.warn('LocalStorage error:', e);
    }
  }, [procurementOrders]);

  useEffect(() => {
    try {
      localStorage.setItem('demandx_inventory_overrides', JSON.stringify(inventoryOverrides));
    } catch (e) {
      console.warn('LocalStorage error:', e);
    }
  }, [inventoryOverrides]);

  // CUSTOMER ORDER WORKFLOW
  const addCustomerOrder = useCallback(
    async (orderData: Omit<CustomerOrder, 'id'>): Promise<string> => {
      let docId = `ORDER_${Date.now()}`;
      try {
        docId = await addCustomerOrderDoc(orderData);
      } catch (err: any) {
        if (err?.message?.includes('Insufficient stock')) {
          throw err;
        }
        console.warn('Firestore transaction fallback for customer order:', err);
      }

      const newOrder: CustomerOrder = {
        id: docId.startsWith('ORDER_') ? `#DX-${Math.floor(1000 + Math.random() * 9000)}` : docId,
        ...orderData,
        customerName: orderData.customerName || currentUser?.displayName || 'Durga Prasad',
        createdAt: new Date().toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }),
      };

      setCustomerOrders((prev) => [newOrder, ...prev]);

      // Deduct retailer inventory
      setInventoryOverrides((prev) => {
        const copy = { ...prev };
        for (const item of orderData.items) {
          copy[item.productId] = (copy[item.productId] || 0) - item.quantity;
        }
        return copy;
      });

      return newOrder.id || docId;
    },
    [currentUser]
  );

  // RETAILER PROCUREMENT WORKFLOW
  const createRetailerStockOrder = useCallback(
    async (
      items: RetailerProcurementItem[],
      supplierId: string = 'GUNTUR_SUPPLIER_HUB',
      supplierName: string = 'Guntur Spice Traders & Exporters',
      retailerId: string = 'GUNTUR_STORE_01',
      retailerName: string = 'My Store - Guntur, AP'
    ): Promise<string> => {
      const totalAmount = items.reduce((sum, i) => sum + i.price * i.quantity, 0);
      const orderData: Omit<RetailerProcurementOrder, 'id'> = {
        retailerId,
        retailerName,
        supplierId,
        supplierName,
        items,
        totalAmount,
        status: 'Pending',
        createdAt: new Date().toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }),
      };

      const docId = await addProcurementOrderDoc(orderData);
      const newPO: RetailerProcurementOrder = {
        id: docId.startsWith('PO_') ? `#PO-${Math.floor(1000 + Math.random() * 9000)}` : docId,
        ...orderData,
      };

      setProcurementOrders((prev) => [newPO, ...prev]);
      return newPO.id || docId;
    },
    []
  );

  // SUPPLIER FULFILLMENT WORKFLOW
  const fulfillSupplierOrder = useCallback(async (orderId: string): Promise<void> => {
    const target = procurementOrders.find((p) => p.id === orderId);
    if (!target) return;

    await updateProcurementOrderStatusDoc(
      orderId,
      'Dispatched',
      target.retailerId,
      target.items
    );

    const nowStr = new Date().toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });

    setProcurementOrders((prev) =>
      prev.map((po) =>
        po.id === orderId
          ? { ...po, status: 'Dispatched', dispatchedAt: nowStr }
          : po
      )
    );

    // Replenish retailer inventory stock
    setInventoryOverrides((prev) => {
      const copy = { ...prev };
      for (const item of target.items) {
        copy[item.productId] = (copy[item.productId] || 0) + item.quantity;
      }
      return copy;
    });
  }, [procurementOrders]);

  // INVENTORY HELPERS
  const updateInventory = useCallback((productId: string, deltaQuantity: number) => {
    setInventoryOverrides((prev) => ({
      ...prev,
      [productId]: (prev[productId] || 0) + deltaQuantity,
    }));
  }, []);

  const getRetailerInventory = useCallback(
    (productId: string, baseStock: number): number => {
      const delta = inventoryOverrides[productId] || 0;
      return Math.max(0, baseStock + delta);
    },
    [inventoryOverrides]
  );

  // GETTER HELPERS FOR DASHBOARDS
  const getCustomerOrders = useCallback(
    (retailerId?: string): CustomerOrder[] => {
      if (!retailerId) return customerOrders;
      return customerOrders.filter((o) => o.retailerId === retailerId);
    },
    [customerOrders]
  );

  const getRetailerProcurementOrders = useCallback(
    (retailerId?: string): RetailerProcurementOrder[] => {
      if (!retailerId) return procurementOrders;
      return procurementOrders.filter((po) => po.retailerId === retailerId);
    },
    [procurementOrders]
  );

  const getSupplierBuyerRequests = useCallback(
    (supplierId?: string): RetailerProcurementOrder[] => {
      if (!supplierId) return procurementOrders;
      return procurementOrders.filter((po) => po.supplierId === supplierId);
    },
    [procurementOrders]
  );

  return (
    <SupplyChainContext.Provider
      value={{
        customerOrders,
        procurementOrders,
        inventoryOverrides,
        addCustomerOrder,
        createRetailerStockOrder,
        fulfillSupplierOrder,
        updateInventory,
        getRetailerInventory,
        getCustomerOrders,
        getRetailerProcurementOrders,
        getSupplierBuyerRequests,
      }}
    >
      {children}
    </SupplyChainContext.Provider>
  );
};

export const useSupplyChain = () => {
  const ctx = useContext(SupplyChainContext);
  if (!ctx) {
    throw new Error('useSupplyChain must be used within a SupplyChainProvider');
  }
  return ctx;
};
