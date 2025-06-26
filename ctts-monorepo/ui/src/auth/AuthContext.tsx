import React, { createContext, useState } from 'react';

export type Role = 'Public' | 'Trainer' | 'Admin';

interface AuthContextValue {
  role: Role;
  login: (role: Role) => void;
}

export const AuthContext = createContext<AuthContextValue>({
  role: 'Public',
  login: () => {},
});

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [role, setRole] = useState<Role>('Public');
  const login = (r: Role) => setRole(r);
  return <AuthContext.Provider value={{ role, login }}>{children}</AuthContext.Provider>;
};
