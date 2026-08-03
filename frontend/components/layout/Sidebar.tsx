"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const menu = [
    {
        label: "Dashboard",
        href: "/dashboard"
    },
    {
        label: "Campaigns",
        href: "/campaigns"
    },
    {
        label: "Contacts",
        href: "/contacts"
    },
    {
        label: "Imports",
        href: "/imports"
    }
];


export default function Sidebar() {

    const pathname = usePathname();


    return (
        <aside className="w-64 min-h-screen bg-white border-r">

            <div className="h-16 flex items-center px-6 border-b">
                <h1 className="text-xl font-bold">
                    CTA Manager
                </h1>
            </div>

            <nav className="p-4 space-y-2">

                {menu.map((item) => {

                    const active = pathname.startsWith(item.href);

                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={`
                                block px-4 py-3 rounded-lg transition
                                ${active
                                    ? "bg-blue-100 text-blue-700 font-medium"
                                    : "text-gray-600 hover:bg-gray-100"
                                }
                            `}
                        >
                            {item.label}
                        </Link>
                    );

                })}

            </nav>

        </aside>
    );
}