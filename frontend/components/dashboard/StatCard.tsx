interface Props {
    title: string;
    value: number;
    description?: string;
}


export default function StatCard({
    title,
    value,
    description
}: Props) {

    return (
        <div className="bg-white border rounded-xl p-6 shadow-sm">
            <p className="text-sm text-gray-500">
                {title}
            </p>

            <p className="text-3xl font-bold mt-2">
                {value}
            </p>

            {description && (
                <p className="text-sm text-gray-500 mt-2">
                    {description}
                </p>
            )}
        </div>
    );
}