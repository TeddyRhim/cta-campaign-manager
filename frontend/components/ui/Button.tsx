interface Props {
    children: React.ReactNode;
    type?: "button" | "submit";
    onClick?: () => void;
}


export default function Button({
    children,
    type = "button",
    onClick
}: Props) {

    return (
        <button
            type={type}
            onClick={onClick}
            className="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition"
        >
            {children}
        </button>
    );
}